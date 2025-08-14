import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

stats_df = pd.read_csv('generated_data/stats_data.csv', index_col=False)
schedule_df = pd.read_csv('shootout_data.csv', index_col=False)
schedule_df['Date'] = schedule_df['Date'].str.replace("-", "")

nhl_teams = {
    'Anaheim Ducks': 'ANA',
    'Arizona Coyotes': 'ARI',
    'Boston Bruins': 'BOS',
    'Buffalo Sabres': 'BUF',
    'Calgary Flames': 'CGY',
    'Carolina Hurricanes': 'CAR',
    'Chicago Blackhawks': 'CHI',
    'Colorado Avalanche': 'COL',
    'Columbus Blue Jackets': 'CBJ',
    'Dallas Stars': 'DAL',
    'Detroit Red Wings': 'DET',
    'Edmonton Oilers': 'EDM',
    'Florida Panthers': 'FLA',
    'Los Angeles Kings': 'LAK',
    'Minnesota Wild': 'MIN',
    'Montreal Canadiens': 'MTL',
    'Nashville Predators': 'NSH',
    'New Jersey Devils': 'NJD',
    'New York Islanders': 'NYI',
    'New York Rangers': 'NYR',
    'Ottawa Senators': 'OTT',
    'Philadelphia Flyers': 'PHI',
    'Pittsburgh Penguins': 'PIT',
    'San Jose Sharks': 'SJS',
    'St. Louis Blues': 'STL',
    'Tampa Bay Lightning': 'TBL',
    'Toronto Maple Leafs': 'TOR',
    'Vancouver Canucks': 'VAN',
    'Vegas Golden Knights': 'VGK',
    'Washington Capitals': 'WSH',
    'Winnipeg Jets': 'WPG',
    'Atlanta Thrashers': 'ATL',
    'Phoenix Coyotes': 'ARI',
    'Montréal Canadiens': 'MTL',
    'Utah Hockey Club': 'UTA',
    'Seattle Kraken': 'SEA'
}

schedule_df["Visitor"] = schedule_df["Visitor"].map(nhl_teams).fillna("NaN")
schedule_df["Home"]    = schedule_df["Home"].map(nhl_teams).fillna("NaN")

visitor_df = schedule_df.rename(columns={
    "Date": "gameDate",
    "Visitor": "playerTeam",
    "awayGoals": "goalsForFixed",
    "homeGoals": "goalsAgainstFixed"   
})[['gameDate', 'playerTeam', 'goalsForFixed', 'goalsAgainstFixed']]

home_df = schedule_df.rename(columns={
    "Date": "gameDate",
    "Home": "playerTeam",
    "homeGoals": "goalsForFixed",      
    "awayGoals": "goalsAgainstFixed"     
})[['gameDate', 'playerTeam', 'goalsForFixed', 'goalsAgainstFixed']]

schedule_df = pd.concat([visitor_df, home_df])

stats_df["gameDate"] = stats_df["gameDate"].astype(str)

temp_df = stats_df.merge(schedule_df, on=["gameDate", "playerTeam"], how="left")
temp_df = temp_df[temp_df['goalsFor'] == temp_df['goalsAgainst']]
temp_df = temp_df.dropna()

stats_df = stats_df.merge(
    temp_df[['gameId', 'playerTeam', 'goalsForFixed', 'goalsAgainstFixed']],
    on=['gameId', 'playerTeam'],
    how='left'
)

stats_df.loc[stats_df['goalsForFixed'].notna(), 'goalsFor'] = stats_df.loc[stats_df['goalsForFixed'].notna(), 'goalsForFixed']

stats_df.loc[stats_df['goalsAgainstFixed'].notna(), 'goalsAgainst'] = stats_df.loc[stats_df['goalsAgainstFixed'].notna(), 'goalsAgainstFixed']

stats_df = stats_df.drop(columns=['goalsForFixed', 'goalsAgainstFixed'])

stats_df['win'] = stats_df['goalsFor'] > stats_df['goalsAgainst']

stats_df['win'] = stats_df['win'].astype(int)

stats_df['svp'] = 1 - (stats_df['goalsAgainst'] / stats_df['shotsOnGoalAgainst'])

def last_5_mean(s):
    return s.rolling(window=5, min_periods=1).sum().shift(1).fillna(0)
stats_df['last_5'] = stats_df.groupby(['playerTeam', 'season'])['win'].transform(last_5_mean)

stats_df['namedmerged'] = stats_df['playerTeam'] + stats_df['opposingTeam'] + stats_df['season'].astype(str)

stats_df['headtohead'] = (
    stats_df.groupby('namedmerged')['win']
    .expanding()
    .sum()
    .shift(1)
    .reset_index(level=0, drop=True)
    .fillna(0)
)

stats_df = stats_df.sort_values(by=['namedmerged', 'gameDate'])

first_games = stats_df.groupby(['namedmerged']).head(1).index

cols_to_zero = ['headtohead']

stats_df = stats_df.drop(columns=['namedmerged'])

stats_df.loc[first_games, cols_to_zero] = 0

stats_df.loc[(stats_df['gameId'] == 2019020876) & (stats_df['playerTeam'] == 'ANA'), ['goalsFor', 'goalsAgainst', 'win']] = [2, 4, 0]
stats_df.loc[(stats_df['gameId'] == 2019020876) & (stats_df['playerTeam'] == 'STL'), ['goalsFor', 'goalsAgainst', 'win']] = [4, 2, 1]

stats_df.to_csv('generated_data/nhl_data_cleaned.csv', index=False)
