import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocessor, helper
from PIL import Image


df = pd.read_csv('Athletes_summer_games.csv')
region_df = pd.read_csv('regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('Olympic-logo.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', "Overall Analysis", 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select Country",country)


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == "Overall":
        st.title(f"Medal Tally in {selected_year}")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(f"{selected_country}  Overall Performance")
    if selected_year != 'Overall' and selected_country != "Overall":
        st.title(f"{selected_country} Performance in {selected_year}")
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]

    st.title("Top Statistics")
    col1 ,col2,col3 = st.columns(3)
    with col1 :
        st.header("Editions")
        st.title(editions)
    with col2 :
        st.header("Hosts")
        st.title(cities)
    with col3 :
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time = helper.data_plot(df,'region')
    fig = px.line(nations_over_time, x='Year', y="region")
    st.title("Participating Nations Over Years")
    st.plotly_chart(fig)

    events_over_time = helper.data_plot(df, 'Event')
    fig = px.line(events_over_time, x='Year', y="Event")
    st.title("Events Over Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_plot(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y="Name", labels={
                     "Name": "No of Athletes",
                 })

    st.title("Athletes Participation Over Years")
    st.plotly_chart(fig)

    st.title("Number of Events Over Time for Every Sport")
    fig , ax = plt.subplots(figsize = (25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    x = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(x,annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox("Select a Sport",sport_list)
    x = helper.most_successfull(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a Country",country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(f"{selected_country} Medal Tally of over the Years")
    st.plotly_chart(fig)
    st.title(f"Top 15 Athletes of {selected_country}")
    top15_df = helper.most_successfull_country_wise(df,selected_country)
    st.table(top15_df)

    pt = helper.country_pivot(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 25))
    st.title(f"{selected_country} excels in the following Sports")
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(['Name', 'region'])
    st.title("Distibution of Age")
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False,show_rug=False)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=500)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title("Participation of Male and Female over Years")
    dfmf = df.drop_duplicates(['Year', 'Name'])[['Year', 'Sex']].value_counts().reset_index().sort_values(by='Year')
    dfmf.rename(columns={0: "Athletes"}, inplace=True)
    fig = px.line(dfmf, x='Year', y='Athletes',color='Sex', color_discrete_sequence=["#C55D4B","#ff90ff"])
    st.plotly_chart(fig)