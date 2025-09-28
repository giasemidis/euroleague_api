import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import (
    raise_error,
    get_requests
)


class GameStats(EuroLeagueData):
    """
    A class for getting the game related stats and data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_game_data(
        self,
        season: int,
        game_code: int,
        endpoint: str
    ) -> pd.DataFrame:
        """
        A wrapper function for getting game-level data.

        Args:

            season (int): The start year of the season

            game_code (int): The game code of the game of interest.
                Find the game code from Euroleague's website

            endpoint (str): The type of game data, available variables:
                - report
                - stats
                - teamsComparison

        Raises:

            ValueError: If input endpoint is not applicable.

        Returns:

            pd.DataFrame: A dataframe with the game data.
        """
        game_endpoints = ["report", "stats", "teamsComparison"]

        raise_error(endpoint, "Statistic type", game_endpoints, False)

        url_ = self.make_season_game_url(season, game_code, endpoint)
        r = get_requests(url_)

        data = r.json()
        df = pd.json_normalize(data)
        df.insert(0, "Season", season)
        if "gameCode" in df.columns:
            df.rename(columns={"gameCode": "Gamecode"}, inplace=True)
        else:
            df.insert(1, "Gamecode", game_code)
        if "round" in df.columns:
            df.rename(columns={"round": "Round"}, inplace=True)

        return df

    def get_game_report(self, season: int, game_code: int) -> pd.DataFrame:
        """
        Get game report data for a game

        Args:
            season (int): The start year of the season
            game_code (int): The game code of the game of interest. It can be
                found on Euroleague's website.

        Returns:
            pd.DataFrame: A dataframw with the game report data
        """
        df = self.get_game_data(season, game_code, "report")
        return df

    def get_game_report_round(
        self, season: int, round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the game report data
        of *all* games in a single round

        Args:
            season (int): The start year of the season
            round_number (int): The round of the season

        Returns:

            pd.DataFrame: A dataframe with the game report data of
                all games in a single round
        """
        data_df = self.get_round_data_from_game_data(
            season, round_number, self.get_game_report)
        return data_df

    def get_game_reports_single_season(self, season: int) -> pd.DataFrame:
        """
        Get game report data for *all* games in a single season

        Args:
            season (int): The start year of the season

        Returns:
            pd.DataFrame: A dataframe with game report data
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_report)
        return data_df

    def get_game_reports_range_seasons(
        self,
        start_season: int,
        end_season: int
    ) -> pd.DataFrame:
        """
        Get game report data for *all* games in a range of seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with game report data
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_report)
        return df

    def get_game_stats(self, season: int, game_code: int) -> pd.DataFrame:
        """
        Get game stats data for single game

        Args:

            season (int): The start year of the season

            game_code (int): The game code of the game of interest. It can be
                found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with the games' stats data
        """
        df = self.get_game_data(season, game_code, "stats")
        return df

    def get_game_stats_round(
        self, season: int, round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the game stats data
        of *all* games in a single round

        Args:
            season (int): The start year of the season
            round_number (int): The round of the season

        Returns:

            pd.DataFrame: A dataframe with the game stats of
                all games in a single round
        """
        data_df = self.get_round_data_from_game_data(
            season, round_number, self.get_game_stats)
        return data_df

    def get_game_stats_single_season(self, season: int) -> pd.DataFrame:
        """
        Get game stats data for *all* games in a single season

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the games' stats data
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_stats)
        return data_df

    def get_game_stats_range_seasons(
        self,
        start_season: int,
        end_season: int
    ) -> pd.DataFrame:
        """
        Get game stats data for *all* games in a range of seasons

        Args:

            start_season (int): The start year of the start season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with the games' stats data
        """
        df = self.get_range_seasons_data(
            start_season, end_season, self.get_game_stats)
        return df

    def get_game_teams_comparison(
        self,
        season: int,
        game_code: int
    ) -> pd.DataFrame:
        """
        A function that gets the "teams comparison" game stats for a single
        game. This is the *pre-game* stats. Hence gamecodes of round 1 of each
        season are not available.

        Args:

            season (int): The start year of the season

            game_code (int): The game code of the game of interest. It can be
                found on Euroleague's website.

        Returns:

            pd.DataFrame: A dataframe with games teams comparison stats
        """
        df = self.get_game_data(season, game_code, "teamsComparison")
        return df

    def get_game_teams_comparison_round(
        self, season: int, round_number: int
    ) -> pd.DataFrame:
        """
        A function that gets the "teams comparison" game stats
        of *all* games in a single round

        Args:
            season (int): The start year of the season
            round_number (int): The round of the season

        Returns:

            pd.DataFrame: A dataframe with the "teams comparison" game stats of
                all games in a single round
        """
        data_df = self.get_round_data_from_game_data(
            season, round_number, self.get_game_teams_comparison)
        return data_df

    def get_game_teams_comparison_single_season(
            self, season: int) -> pd.DataFrame:
        """
        A function that gets the pre-grame "teams comparison" game stats for
        *all* games in a single season.

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with games teams comparison stats
        """
        data_df = self.get_season_data_from_game_data(
            season, self.get_game_teams_comparison)
        return data_df

    def get_game_teams_comparison_range_seasons(
        self,
        start_season: int,
        end_season: int
    ) -> pd.DataFrame:
        """
        A function that gets the pre-game "teams comparison" game stats for
        *all* in a range seasons

        Args:

            start_season (int): The start year of the star season

            end_season (int): The start year of the end season

        Returns:

            pd.DataFrame: A dataframe with games teams comparison stats
        """
        df = self.get_range_seasons_data(
            start_season,
            end_season,
            self.get_game_teams_comparison
        )
        return df
