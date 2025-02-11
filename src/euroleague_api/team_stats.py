from typing import Optional
import pandas as pd
import numpy as np
from .EuroLeagueData import EuroLeagueData
from .boxscore_data import BoxScoreData
from .utils import (
    raise_error,
    get_requests
)


class TeamStats(EuroLeagueData):
    """
    A class for getting team-level stats and data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_team_stats(
        self,
        endpoint: str,
        params: dict = {},
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        A wrapper functions for collecting teams' stats.
        Allows for three types of data:
        - all seasons
        - single season
        - range of seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            params (Dict[str, Union[str, int]]): A dictionary of the parmaters
                for the get request.

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Raises:

            ValueError: If the endpoint is not applicable

            ValueError: If the phase_type_code is not applicable

            ValueError: If the statistic_mode is not applicable

        Returns:

            pd.DataFrame: A dataframe with the teams' stats.
        """

        available_endpoints = [
            "traditional", "advanced",
            "opponentsTraditional", "opponentsAdvanced"
        ]
        available_phase_type_code = ["RS", "PO", "FF"]
        available_stat_mode = ["PerGame", "Accumulated"]

        raise_error(
            endpoint, "Statistic type", available_endpoints, False)
        raise_error(
            statistic_mode, "Statistic Aggregation", available_stat_mode,
            False)
        raise_error(
            phase_type_code, "Phase type code", available_phase_type_code,
            True)

        params["statisticMode"] = statistic_mode
        params["phaseTypeCode"] = phase_type_code
        params["limit"] = 400

        url_ = f"{self.url}/statistics/teams/{endpoint}"

        r = get_requests(url_, params=params)
        data = r.json()
        if data["total"] < len(data["teams"]):
            params["limit"] = len(data["teams"]) + 1
            r = get_requests(url_, params=params)
            data = r.json()
        df = pd.json_normalize(data["teams"])
        return df

    def get_team_stats_all_seasons(
        self,
        endpoint: str,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        A function that gets the team stats for all seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {"SeasonMode": "All"}
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_team_stats_single_season(
        self,
        endpoint: str,
        season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        A function that returns the teams' stats in a single season

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            season (int): The start year of the season

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {
            "SeasonMode": "Single",
            "SeasonCode": f"{self.competition}{season}",
        }
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_team_stats_range_seasons(
        self,
        endpoint: str,
        start_season: int,
        end_season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        A function that returns the teams' stats in a range of seasons

        Args:

            endpoint (str): The type of stats to fetch. Available values:
                - traditional
                - advanced
                - opponentsTraditional
                - opponentsAdvanced

            start_season (int): The start year of the start season

            end_season (int): The end year of the end season

            phase_type_code (Optional[str], optional): The phase of the season,
                available variables:
                - "RS" (regular season)
                - "PO" (play-off)
                - "FF" (final four)
                Defaults to None, which includes all phases.

            statistic_mode (str, optional): The aggregation of statistics,
                available variables:
                - PerGame
                - Accumulated
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the teams' stats
        """
        params = {
            "SeasonMode": "Range",
            "FromSeasonCode": f"{self.competition}{start_season}",
            "ToSeasonCode": f"{self.competition}{end_season}",
        }
        df = self.get_team_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_team_advanced_stats_single_game(self, season: int, gamecode: int):
        """
        In this function we derive team advanced stats from a single game
        that are not provided by the API but can be easily estimated from
        stats that are given from the API, i.e.
            - Number of Possessions
            - Pace
        The formulas and definitions of these stats can be found in
            - [Basketball-reference.com](https://www.basketball-reference.com/about/glossary.html)  # noqa
            - [kenpom](https://kenpom.com/blog/the-possession/)
            - [hackastat](https://hackastat.eu/en/learn-a-stat-possessions-and-pace/)  # noqa

        Args:
            season (int): The start year of the season
            gamecode (int): The game-code of the game of interest.
                It can be found on Euroleague's website.
        """
        boxscoredata = BoxScoreData(competition=self.competition)
        game_bxscr_stats = boxscoredata.get_player_boxscore_stats_data(
            season=season, gamecode=gamecode)
        totals_df = (
            game_bxscr_stats[game_bxscr_stats["Player_ID"] == "Total"]
            .set_index("Team").T
        )
        fga = (totals_df.loc["FieldGoalsAttempted2"] +
               totals_df.loc["FieldGoalsAttempted3"])

        fgm = (totals_df.loc["FieldGoalsMade2"] +
               totals_df.loc["FieldGoalsMade3"])
        possessions_simple = (
            fga
            + 0.44 * (totals_df.loc["FreeThrowsAttempted"])
            - totals_df.loc["OffensiveRebounds"] + totals_df.loc["Turnovers"]
        )

        possessions = (
            fga
            + 0.44 * (totals_df.loc["FreeThrowsAttempted"])
            - 1.07 * (
                totals_df.loc["OffensiveRebounds"] /
                totals_df.loc["DefensiveRebounds", ::-1]
            ) * (fga - fgm)
            + totals_df.loc["Turnovers"]
        )

        df = pd.DataFrame(
            {
                "Possessions (simple)": possessions_simple,
                "Possessions": possessions,
            }
        )
        df.loc["Game"] = [possessions_simple.mean(), possessions.mean()]

        min_played_ls = totals_df.loc["Minutes"].iloc[0].split(":")
        min_played = int(min_played_ls[0]) + float(min_played_ls[1]) / 60
        min_factor = (min_played / 5)

        df["Pace (simple)"] = [
            np.nan, np.nan, 40 * possessions_simple.mean() / min_factor
        ]
        df["Pace"] = [np.nan, np.nan, 40 * possessions.mean() / min_factor]
        df["Season"] = season
        df["Gamecode"] = gamecode
        df["Home"] = [1, 0, np.nan]

        df = df[
            [
                "Season", "Gamecode", "Home",
                "Possessions (simple)", "Possessions",
                "Pace (simple)", "Pace",
            ]
        ]
        return df
