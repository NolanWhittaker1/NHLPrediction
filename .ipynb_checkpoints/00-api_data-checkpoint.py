import pandas as pd
import requests

season_ends = [
    "2025-04-13",
    "2024-04-18",
    "2023-04-14",
    "2022-04-29",
    "2021-05-08",
    "2020-03-11",
    "2019-04-06",
    "2018-04-07",
    "2017-04-09",
    "2016-04-09",
    "2015-04-11",
    "2014-04-13",
    "2013-04-27",
    "2012-04-07",
    "2011-04-10",
    "2010-04-11",
    "2009-04-11"
]

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
    'Phoenix Coyotes': 'PHX',
    'Montréal Canadiens': 'MTL',
    'Utah Hockey Club': 'UTA',
    'Seattle Kraken': 'SEA',
    'Phoenix Coyotes': 'ARI'
}

all_data = []

for date in season_ends:
    url = f"https://api-web.nhle.com/v1/standings/{date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for team in data['standings']:
            all_data.append({"playerTeam": team["teamName"]["default"], "pts": team["points"], "rk": team["leagueSequence"], "season": int(team['date'][:4])-1})
    else:
        print(f"Failed to get data for {date}. Please try again or unzip provided data")

df = pd.DataFrame(all_data)
df["playerTeam"] = df["playerTeam"].map(nhl_teams).fillna(df["playerTeam"])
df.to_csv('generated_Data/season_rank.csv',index=False)
