from json.decoder import JSONDecodeError
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class GamePlayByPlay(EuroLeagueData):

    def get_game_play_by_play_data(
        self,
        season: int,
        gamecode: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of a particular game.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of the game.
        """
        url = "https://live.euroleague.net/api/PlaybyPlay"
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

        periods = [
            'FirstQuarter', 'SecondQuarter', 'ThirdQuarter', 'ForthQuarter',
            'ExtraTime'
        ]
        all_data = []
        for p, period in enumerate(periods):
            if data[period]:
                df = pd.json_normalize(data[period])
                df["PERIOD"] = p + 1
                all_data.append(df)

        play_by_play_df = pd.concat(all_data)
        play_by_play_df['CODETEAM'] = play_by_play_df['CODETEAM'].str.strip()
        play_by_play_df['PLAYER_ID'] = play_by_play_df['PLAYER_ID'].str.strip()
        play_by_play_df.insert(0, 'Season', season)
        play_by_play_df.insert(1, 'Gamecode', gamecode)
        return play_by_play_df

    def get_game_play_by_play_data_single_season(
        self,
        season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a single
        season

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in a single season
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_play_by_play_data)
        return data_df

    def get_game_play_by_play_data_multiple_seasons(
        self, start_season: int, end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a range of
        seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the play-by-play data of all games
                in range of seasons
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_play_by_play_data)
        return df
