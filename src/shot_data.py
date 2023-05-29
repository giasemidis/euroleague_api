import pandas as pd
import requests

MADE_ACTIONS = ['2FGM', '3FGM', 'LAYUPMD', 'DUNK']
MISSES_ACTIONS = ['2FGA', '2FGAB', '3FGA', '3FGAB', 'LAYUPATT']


def get_game_shot_data(season: int, gamecode: int) -> pd.DataFrame:
    """
    Get the shot data of a single game in the season
    """
    url = (
        f"https://live.euroleague.net/api/Points?gamecode={gamecode}"
        f"&seasoncode=E{season}"
    )
    r = requests.get(url)

    if r.status_code != 200:
        print("something went wrong while fetching the data")

    if r.text == '':
        shots_df = None
        print(
            f"No available data found for game-code {gamecode} and season "
            f"{season}"
        )
    else:
        data = r.json()
        shots_df = pd.DataFrame(data['Rows'])
        # team id, player id and action id contain trailing white space
        shots_df['TEAM'] = shots_df['TEAM'].str.strip()
        shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()
        shots_df['ID_ACTION'] = shots_df['ID_ACTION'].str.strip()
        shots_df.insert(0, 'Season', season)
        shots_df.insert(1, 'Gamecode', gamecode)
    return shots_df


def get_season_shot_data(season: int = 2022) -> pd.DataFrame:
    """
    Get the shot data of all games in a season
    """
    data_list = []
    gamecode = 0
    attempt = 0
    while True:
        gamecode += 1
        shots_df = get_game_shot_data(season, gamecode)

        # Due to the ban of Russian teams from Euroleague in 2021
        # this is a hack for not breaking in the first
        # "empty" game, but only after 5 *concecutive*
        # "empty" games
        if shots_df is None:
            attempt += 1
        else:
            attempt = 0
            data_list.append(shots_df)

        if attempt > 5:
            print("No more available game data for this season, break and exit")
            break

    data_df = None
    if data_list:
        data_df = pd.concat(data_list, axis=0)
    return data_df
