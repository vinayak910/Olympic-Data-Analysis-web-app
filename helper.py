import numpy as np

def fetch_medal_tally(df, year , country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    button = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        button =1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if button ==1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending = True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country

def data_plot(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': "Year", 'Year': col}, inplace=True)
    return nations_over_time


def most_successfull(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, right_on="Name", left_on='index', how='left')[[
        'index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': "Name", 'Name_x': 'Medals'}, inplace=True)
    x.reset_index(inplace=True)
    x.drop('index', axis=1, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset= ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_pivot(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset= ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index="Sport", columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successfull_country_wise(df, country):
    temp_df = df.dropna(subset=["Medal"])

    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, right_on="Name", left_on='index', how='left')[[
        'index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': "Name", 'Name_x': 'Medals'}, inplace=True)
    x.reset_index(inplace=True)
    x.drop('index', axis=1, inplace=True)
    return x