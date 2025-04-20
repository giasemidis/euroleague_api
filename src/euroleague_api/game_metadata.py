import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class GameMetadata(EuroLeagueData):

    """
    A class for getting the game related metadata.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def __init__(self, competition_code):
        self.competition_code = competition_code

    def get_game_metadata(self, season, gamecode):
        """
        Retrieves game metadata for a given gamecode.

        Args:
            season (int): The start year of the season.
            gamecode (int): Unique identifier code of the game which can be found on Euroleague's official website.

        Returns:
            pd.DataFrame: A dataframe containing metadata of a game.
        """
        base_url = 'https://live.euroleague.net/api/Header?gamecode={}&seasoncode={}{}&disp='
        url = base_url.format(gamecode, self.competition_code, season)
        response = get_requests(url)

        if response is None:
            raise ValueError(f"Failed to retrieve data for gamecode {gamecode}, season {season}")

        json_content = response.json()
        return pd.json_normalize(json_content)
    
    def get_game_metadata_single_season(self, season):
        """
        A function to retrieve game metadata for all games in a single season.

        Args:
            season (int): The start year of the season.

        Returns:
            pd.DataFrame: A dataframe containing metadata for all games in the given season.
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
