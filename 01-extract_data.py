import pandas as pd

df = pd.read_csv('all_teams.csv')

df = df[df['situation'] == 'all']

df = df[df['playoffGame'] == 0]

df = df.filter(items=['season', 'gameDate', 'gameId', 'playerTeam', 'opposingTeam', 'home_or_away', 'goalsFor', 'goalsAgainst', 'shotsOnGoalFor', 'highDangerShotsFor','highDangerShotsAgainst', 'shotsOnGoalAgainst'])

df['win'] = df['goalsAgainst'] < df['goalsFor']
df['win'] = df['win'].astype(int)

df = df.sort_values(['season', 'playerTeam', 'gameDate'])
df['prev_game'] = df['gameDate'].shift(1, fill_value=0)
df['backtoback'] = df['gameDate'] == df['prev_game'] + 1
df = df.drop(columns='prev_game')

nhl_teams = {
    'S.J': 'SJS',
    'L.A': 'LAK',
    'T.B': 'TBL',
    'N.J': 'NJD'
}

df["playerTeam"] = df["playerTeam"].map(nhl_teams).fillna(df["playerTeam"])
df["opposingTeam"] = df["opposingTeam"].map(nhl_teams).fillna(df["opposingTeam"])

df.to_csv('generated_data/stats_data.csv', index=False)


    









