from typing import Optional
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import (
    raise_error,
    get_requests
)


class TeamStats(EuroLeagueData):
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
        phase_type_code: str,
        statistic_mode: str
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
