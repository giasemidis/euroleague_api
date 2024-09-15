from typing import List
from json.decoder import JSONDecodeError
import pandas as pd
import numpy as np
from .EuroLeagueData import EuroLeagueData
from .utils import (
    get_requests,
    raise_error
)


class BoxScoreData(EuroLeagueData):
    """
    A class for getting box-score data

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_boxscore_data(
        self,
        season: int,
        gamecode: int,
        boxscore_type: str = "ByQuarter"
    ) -> List[dict]:
        """A helper function that gets the boxscore data of a particular data.

        Args:
            season (int): The start year of the season
            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.
            boxscore_type (str, optional): The type of quarter boxscore data.
                Available values:
                - Stats
                - ByQuarter
                - EndOfQuarter
                Defaults to "ByQuarter".

        Raises:
            ValueError: If boxscore_type value is not valid.

        Returns:
            List[dict]: A list of dictionaries with the data.
        """
        url = "https://live.euroleague.net/api/Boxscore"
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
        boxscore_types = ["Stats", "ByQuarter", "EndOfQuarter"]

        if boxscore_type not in boxscore_types:
            raise_error(boxscore_type, "Boxscore", boxscore_types, False)

        return data[boxscore_type]

    def get_game_boxscore_quarter_data(
        self,
        season: int,
        gamecode: int,
        boxscore_type: str = "ByQuarter"
    ) -> pd.DataFrame:
        """
        A function that gets the boxscore quarterly data of a particular game.

        Args:

            season (int): The start year of the season

            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

            boxscore_type (str): The type of quarter boxscore data.
                Available values:
                - ByQuarter
                - EndOfQuarter
                Default: ByQuarter

        Raises:
            ValueError: If boxscore_type value is not valid.

        Returns:

            pd.DataFrame: A dataframe with the boxscore quarter data of the
                game.
        """
        valid_vals = ["ByQuarter", "EndOfQuarter"]
        if boxscore_type not in valid_vals:
            raise_error(boxscore_type, "Boxscore quarter type",
                        valid_vals, False)

        data = self.get_boxscore_data(season, gamecode, boxscore_type)
        df = pd.json_normalize(data)
        df.insert(0, 'Season', season)
        df.insert(1, 'Gamecode', gamecode)
        return df

    def get_player_boxscore_stats_data(
        self,
        season: int,
        gamecode: int
    ) -> pd.DataFrame:
        """
        The players' and team's total stats of a particular game.

        Args:
            season (int): The start year of the season
            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.

        Returns:
            pd.DataFrame: A dataframe with home and away team player stats
        """

        def dict_to_df_bx(datadict, home=1):
            playerstats_df = pd.json_normalize(datadict["PlayersStats"])
            teamstats_df = pd.json_normalize(datadict["tmr"])
            totalstats_df = pd.json_normalize(datadict["totr"])
            df = pd.concat(
                [
                    # fix types to avoid pandas futurewarning
                    playerstats_df.astype(teamstats_df.dtypes),
                    teamstats_df,
                    totalstats_df
                ],
                ignore_index=True
            )
            if "Plusminus" in df.columns:
                # replace None entries and fix data type
                # this behaviour used to be automatic, but since version
                # 2.1.0, pandas throws a futurewarning
                df.loc[df["Plusminus"].isnull(), "Plusminus"] = np.nan
                df["Plusminus"] = df["Plusminus"].astype(float)
            df.iloc[-2:, 0] = ["Team", "Total"]  # type: ignore
            df.iloc[-2:, 5] = ["Team", "Total"]  # type: ignore
            df["Team"] = df["Team"].ffill()
            df.insert(0, 'Season', season)
            df.insert(1, 'Gamecode', gamecode)
            df.insert(2, "Home", home)
            return df

        data = self.get_boxscore_data(season, gamecode, "Stats")

        home_df = dict_to_df_bx(data[0], home=1)
        away_df = dict_to_df_bx(data[1], home=0)

        df = pd.concat([home_df, away_df], axis=0, ignore_index=True)
        return df

    def get_game_boxscore_quarter_data_single_season(
        self,
        season: int,
        boxscore_type: str = "ByQuarter"
    ) -> pd.DataFrame:
        """
        A function that gets the boxscore quarter data of *all* games in a
        single season

        Args:

            season (int): The start year of the season

            boxscore_type (str): The type of quarter boxscore data.
            Available values:
                - ByQuarter
                - EndOfQuarter
            Default: ByQuarter

        Returns:

            pd.DataFrame: A dataframe with the boxscore quarter data of all
                games in a single season
        """
        get_game_boxscore_quarter_data_ = (
            lambda season, gamecode: self.get_game_boxscore_quarter_data(
                season, gamecode, boxscore_type)
        )
        data_df = self.get_season_data_from_game_data(
            season, get_game_boxscore_quarter_data_)
        return data_df

    def get_game_boxscore_quarter_data_multiple_seasons(
        self,
        start_season: int,
        end_season: int,
        boxscore_type: str = "ByQuarter"
    ) -> pd.DataFrame:
        """
        A function that gets the play-by-play data of *all* games in a range of
        seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

            boxscore_type (str): The type of quarter boxscore data.
                Available values:
                - ByQuarter
                - EndOfQuarter
                Default: ByQuarter

        Returns:

            pd.DataFrame: A dataframe with the boxscore quarter data of all
                games in range of seasons
        """
        get_game_boxscore_quarter_data_ = (
            lambda season, gamecode: self.get_game_boxscore_quarter_data(
                season, gamecode, boxscore_type)
        )
        df = self.get_range_seasons_data(
            start_season, end_season, get_game_boxscore_quarter_data_)
        return df

    def get_player_boxscore_stats_single_season(
        self,
        season: int
    ) -> pd.DataFrame:
        """
        A function that return the player boxscore stats for all games in a
        single season

        Args:
            season (int): The start year of the start season

        Returns:
            pd.DataFrame: A dataframe with home and away team player stats for
                a season
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_player_boxscore_stats_data)
        return data_df

    def get_player_boxscore_stats_multiple_seasons(
        self,
        start_season: int,
        end_season: int
    ) -> pd.DataFrame:
        """
        A function that return the player boxscore stats for all games in
        multiple season

        Args:
            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:
            pd.DataFrame: A dataframe with home and away team player stats for
                a season
        """
        data_df = self.get_range_seasons_data(
            start_season, end_season, self.get_player_boxscore_stats_data)
        return data_df
