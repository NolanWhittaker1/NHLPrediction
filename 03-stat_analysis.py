import pandas as pd
import numpy as np
import scipy as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

stat_data = pd.read_csv('generated_data/nhl_data_cleaned.csv')
rank_data = pd.read_csv('generated_data/season_rank.csv')

stat_season_totals = stat_data.groupby(['playerTeam', 'season']).agg({'goalsFor': 'sum', 'goalsAgainst': 'sum', 'shotsOnGoalFor': 'sum', 'highDangerShotsFor': 'sum', 'highDangerShotsAgainst': 'sum', 'shotsOnGoalAgainst': 'sum', 'svp': 'mean'}).reset_index()

stat_season_totals = stat_season_totals.merge(rank_data, on=['playerTeam', 'season'], how='left')

stat_season_totals = stat_season_totals.sort_values(by=['season','rk'])

sns.set_theme(style="whitegrid")

print("Rank and Goals Correlation: ", stats.linregress(stat_season_totals['rk'], stat_season_totals['goalsFor']).rvalue)
g = sns.lmplot(
    x='rk',
    y='goalsFor',
    data=stat_season_totals,
    hue='season',
)

g.set_axis_labels("Rank", "Goals For")
g.set_titles("goalsFor vs Season Rank")
g.set(xlim=(33, 0))
gr = g.fig
gr.savefig('images/rankgoals.png')

print("Rank and High Danger Shot Correlation: ", stats.linregress(stat_season_totals['rk'], stat_season_totals['highDangerShotsFor']).rvalue)
g = sns.lmplot(
    x='rk',
    y='highDangerShotsFor',
    data=stat_season_totals,
    hue='season',
)
g.set(xlim=(33, 0))
g.set_axis_labels("Rank", "High Danger Chances")
g.set_titles("High Danger Chances vs Season Rank")

gr = g.fig
gr.savefig('images/rankchances.png')

print("Rank and Goals Against Correlation: ", stats.linregress(stat_season_totals['rk'], stat_season_totals['goalsAgainst']).rvalue)
g = sns.lmplot(
    x='rk',
    y='goalsAgainst',
    data=stat_season_totals,
    hue='season',
)
g.set(xlim=(33, 0))
g.set_axis_labels("Rank", "Goals Against")
g.set_titles("goalsAgainst vs Season Rank")

gr = g.fig
gr.savefig('images/rankagainst.png')

print("Rank and Save Percentage Correlation: ", stats.linregress(stat_season_totals['rk'], stat_season_totals['svp']).rvalue)
g = sns.lmplot(
    x='rk',
    y='svp',
    data=stat_season_totals,
    hue='season',
)
g.set_axis_labels("Rank", "Save Percentage")
g.set(xlim=(33, 0))
g.set_titles("Save Percentage vs Season Rank")
gr = g.fig
gr.savefig('images/ranksave.png')

plt.figure()

b2b = stat_data[stat_data['backtoback'] == True]
lose_b2b = b2b[b2b['win'] == False].groupby('season').size().rename('wins')
win_b2b = b2b[b2b['win'] == True].groupby('season').size().rename('wins')
b2b_data = pd.DataFrame({'lose': lose_b2b, 'win': win_b2b}).reset_index()
b2b_melted = b2b_data.melt(id_vars='season', value_vars=['win', 'lose'], var_name='result', value_name='count')
g = sns.barplot(
    x='season',
    y='count',
    hue='result',
    data=b2b_melted
)
g.tick_params(axis='x', rotation=90)
# Adapted from https://stackoverflow.com/questions/30490740/move-legend-outside-figure-in-seaborn-tsplot
g.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
g.figure.savefig('images/backtoback.png')
plt.figure()

home_win = stat_data[(stat_data['win'] == True) & (stat_data['home_or_away'] == 'HOME')].groupby('season').size().rename('wins')
away_win = stat_data[(stat_data['win'] == True) & (stat_data['home_or_away'] == 'AWAY')].groupby('season').size().rename('wins')
home_away_data = pd.DataFrame({'home': home_win , 'away': away_win}).reset_index()
home_away_melted = home_away_data.melt(id_vars='season', value_vars=['home', 'away'], var_name='result', value_name='count')
g = sns.barplot(
    x='season',
    y='count',
    hue='result',
    data=home_away_melted
)

g.tick_params(axis='x', rotation=90)
# Adapted from https://stackoverflow.com/questions/30490740/move-legend-outside-figure-in-seaborn-tsplot
g.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
g.figure.savefig('images/homeaway.png')










