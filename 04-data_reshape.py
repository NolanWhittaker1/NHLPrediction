import pandas as pd

df = pd.read_csv('generated_data/nhl_data_cleaned.csv')

df['win'] = df['win'].astype(int)

df['svp'] = 1 - (df['goalsAgainst'] / df['shotsOnGoalAgainst'])

def sum_all_of_season(s):
    return s.expanding().mean().shift(1).fillna(0)

df['xSA'] = df.groupby(['playerTeam', 'season'])['shotsOnGoalAgainst'].transform(sum_all_of_season)
df['xSF'] = df.groupby(['playerTeam', 'season'])['shotsOnGoalFor'].transform(sum_all_of_season)
df['xHSA'] = df.groupby(['playerTeam', 'season'])['highDangerShotsAgainst'].transform(sum_all_of_season)
df['xHSF'] = df.groupby(['playerTeam', 'season'])['highDangerShotsFor'].transform(sum_all_of_season)
df['xGF'] = df.groupby(['playerTeam', 'season'])['goalsFor'].transform(sum_all_of_season)
df['xGA'] = df.groupby(['playerTeam', 'season'])['goalsAgainst'].transform(sum_all_of_season)
df['xSV'] = df.groupby(['playerTeam', 'season'])['svp'].transform(sum_all_of_season)
df['xWin'] = df.groupby(['playerTeam', 'season'])['win'].transform(sum_all_of_season)
df['xSvp'] = df.groupby(['playerTeam', 'season'])['svp'].transform(sum_all_of_season)

df = df.drop(columns=['svp', 'goalsFor', 'goalsAgainst', 'shotsOnGoalFor', 'highDangerShotsFor', 'highDangerShotsAgainst', 'shotsOnGoalAgainst'])

first_games = df.groupby(['playerTeam', 'season']).head(1).index

cols_to_zero = ['xSA', 'xSF','xHSA', 'xHSF', 'xGF', 'xGA', 'xSV', 'xWin', 'xSvp']

df.loc[first_games, cols_to_zero] = 0

home_df = df[df['home_or_away'] == 'HOME'].copy()
away_df = df[df['home_or_away'] == 'AWAY'].copy()

away_df = away_df.rename(columns={
    'xSA': 'o_xSA', 'xSF': 'o_xSF', 'xGF': 'o_xGF', 'xGA': 'o_xGA',
    'xSV': 'o_xSV', 'xWin': 'o_xWin', 'xSvp': 'o_xSvp', 'backtoback': 'o_backtoback', 'headtohead': 'o_headtohead'
})

away_df = away_df[['gameId', 'o_backtoback','o_headtohead', 'o_xSA', 'o_xSF', 'o_xGF', 'o_xGA', 'o_xSV', 'o_xWin', 'o_xSvp']]

df_merged = home_df.merge(away_df, on='gameId')

df = df_merged.sort_values(by=['gameDate', 'gameId'])

df.to_csv('generated_data/ml_shaped_data.csv', index=False)



