from json.decoder import JSONDecodeError
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class GameMetadata(EuroLeagueData):

    """
    A class for getting the game related metadata, such as
    stadum, capacity and referee names.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_game_metadata(self, season: int, gamecode: int) -> pd.DataFrame:
        """
        Retrieves game metadata for a given gamecode, such as stadium,
        capacity and referee names.

        Args:
            season (int): The start year of the season.
            gamecode (int): Unique identifier code of the game which can be
                found on Euroleague's official website.

        Returns:
            pd.DataFrame: A dataframe containing metadata of a game.
        """
        url = "https://live.euroleague.net/api/Header"
        params = {
            "gamecode": gamecode,
            "seasoncode": f"{self.competition}{season}"
        }
        r = get_requests(url, params=params)

        try:
            data = r.json()
        except JSONDecodeError as exc:
            raise ValueError(
                f"Game code, {gamecode}, season {season} "
                "did not return any data."
            ) from exc
        metadata_df = pd.json_normalize(data)
        metadata_df.insert(0, 'Season', season)
        metadata_df.insert(1, 'Gamecode', gamecode)
        metadata_df["Round"] = metadata_df["Round"].astype(int)
        return metadata_df

    def get_game_metadata_round(
        self, season: int, round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the metadata of all games in a single round.

        Args:
            season (int): The start year of the season.
            round_number (int): The round of the season.

        Returns:
            pd.DataFrame: A dataframe with the metadata of all games in a
                single round.
        """
        df = self.get_round_data_from_game_data(
            season=season,
            round_number=round_number,
            fun=self.get_game_metadata
        )
        return df

    def get_game_metadata_single_season(self, season: int) -> pd.DataFrame:
        """
        A function to retrieve game metadata for all games in a single season.

        Args:
            season (int): The start year of the season.

        Returns:
            pd.DataFrame: A dataframe containing metadata for all games
                in the given season.
        """

        single_season_metadata_df = self.get_season_data_from_game_data(
            season, self.get_game_metadata
        )
        return single_season_metadata_df

    def get_game_metadata_multiple_seasons(
        self, start_season: int, end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the metadata of *all* games in a range of seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the metadata of all games in range
                of seasons
        """
        metadata_df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_metadata)
        return metadata_df
