from json.decoder import JSONDecodeError
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class ShotData(EuroLeagueData):
    """
    A class for getting shot data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """
    # MADE_ACTIONS = ['2FGM', '3FGM', 'LAYUPMD', 'DUNK']
    # MISSES_ACTIONS = ['2FGA', '2FGAB', '3FGA', '3FGAB', 'LAYUPATT']

    def get_game_shot_data(self, season: int, gamecode: int) -> pd.DataFrame:
        """
        A function that gets the shot data of a particular game.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the shot data of the game.
        """
        url = "https://live.euroleague.net/api/Points"
        params = {
            "gamecode": gamecode,
            "seasoncode": f"{self.competition}{season}"
        }
        r = get_requests(url, params=params)

        try:
            data = r.json()
        except JSONDecodeError:
            raise ValueError(
                f"Game code, {gamecode}, did not return any data.")

        shots_df = pd.DataFrame(data['Rows'])
        # team id, player id and action id contain trailing white space
        if not shots_df.empty:
            shots_df['TEAM'] = shots_df['TEAM'].str.strip()
            shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()
            shots_df['ID_ACTION'] = shots_df['ID_ACTION'].str.strip()
            shots_df.insert(0, 'Season', season)
            shots_df.insert(1, 'Gamecode', gamecode)
        return shots_df

    def get_game_shot_data_single_season(self, season: int) -> pd.DataFrame:
        """
        A function that gets the shot data of *all* games in a single season

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the shot data of all games in a
                single season
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_shot_data)
        return data_df

    def get_game_shot_data_multiple_seasons(
        self, start_season: int, end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the shot data of *all* games in a range of seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the shot data of all games in range
                of seasons
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_shot_data)
        return df
