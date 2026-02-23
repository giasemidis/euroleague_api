from typing import Optional
import pandas as pd
from .EuroLeagueData import EuroLeagueData
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

    def get_team_stats_leaders(
        self,
        params: dict = {},
        stat_category: str | None = None,
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        A wrapper function for collecting the leading team in a given
        stat category.

        Args:

            params (Dict[str, Union[str, int]]): A dictionary of parameters
                for the get request.

            top_n (int): The number of top N teams to return.
                Defaults to 200.

            stat_category (str): The stat category. Available values:
                - None # (time played)
                - Valuation
                - Score
                - TotalRebounds
                - OffensiveRebounds
                - DefensiveRebounds
                - Assistances
                - Steals
                - BlocksFavour
                - BlocksAgainst
                - Turnovers
                - FoulsReceived
                - FoulsCommited
                - FreeThrowsMade
                - FreeThrowsAttempted
                - FreeThrowsPercent
                - FieldGoalsMade2
                - FieldGoalsAttempted2
                - FieldGoals2Percent
                - FieldGoalsMade3
                - FieldGoalsAttempted3
                - FieldGoals3Percent
                - FieldGoalsMadeTotal
                - FieldGoalsAttemptedTotal
                - FieldGoalsPercent
                - AccuracyMade
                - AccuracyAttempted
                - AccuracyPercent
                - AssitancesTurnoversRation
                - GamesPlayed
                - GamesStarted
                - TimePlayed
                - Contras
                - Dunks
                - OffensiveReboundPercentage
                - DefensiveReboundPercentage
                - ReboundPercentage
                - EffectiveFeildGoalPercentage
                - TrueShootingPercentage
                - AssistRatio
                - TurnoverRatio
                - FieldGoals2AttemptedRatio
                - FieldGoals3AttemptedRatio
                - FreeThrowRate
                - Possessions
                - GamesWon
                - GamesLost
                - DoubleDoubles
                - TripleDoubles
                - FieldGoalsAttempted2Share
                - FieldGoalsAttempted3Share
                - FreeThrowsAttemptedShare
                - FieldGoalsMade2Share
                - FieldGoalsMade3Share
                - FreeThrowsMadeShare
                - PointsMade2Rate
                - PointsMade3Rate
                - PointsMadeFreeThrowsRate
                - PointsAttempted2Rate
                - PointsAttempted3Rate
                - Age

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
                - PerMinute
                - Per100Possesions
                - PerGameReverse
                - AccumulatedReverse
                Defaults to "PerGame".

            game_type (Optional[str], optional): The type of games to draw the
                top stats from. Available values:
                - HomeGames
                - AwayGames
                - GamesWon
                - GamesLost
                Defaults to None, meaning all games

        Raises:

            ValueError: If the stat_category is not applicable

            ValueError: If the phase_type_code is not applicable

            ValueError: If the statistic_mode is not applicable

            ValueError: If the game_type is not applicable

        Returns:

            pd.DataFrame: A dataframe with the top teams' stats
        """
        avaiable_stat_category = [
            None,  # (time played)
            "Valuation",
            "Score",
            "TotalRebounds",
            "OffensiveRebounds",
            "DefensiveRebounds",
            "Assistances",
            "Steals",
            "BlocksFavour",
            "BlocksAgainst",
            "Turnovers",
            "FoulsReceived",
            "FoulsCommited",
            "FreeThrowsMade",
            "FreeThrowsAttempted",
            "FreeThrowsPercent",
            "FieldGoalsMade2",
            "FieldGoalsAttempted2",
            "FieldGoals2Percent",
            "FieldGoalsMade3",
            "FieldGoalsAttempted3",
            "FieldGoals3Percent",
            "FieldGoalsMadeTotal",
            "FieldGoalsAttemptedTotal",
            "FieldGoalsPercent",
            "AccuracyMade",
            "AccuracyAttempted",
            "AccuracyPercent",
            "AssitancesTurnoversRation",
            "GamesPlayed",
            "GamesStarted",
            "TimePlayed",
            "Contras",
            "Dunks",
            "OffensiveReboundPercentage",
            "DefensiveReboundPercentage",
            "ReboundPercentage",
            "EffectiveFeildGoalPercentage",
            "TrueShootingPercentage",
            "AssistRatio",
            "TurnoverRatio",
            "FieldGoals2AttemptedRatio",
            "FieldGoals3AttemptedRatio",
            "FreeThrowRate",
            "Possessions",
            "GamesWon",
            "GamesLost",
            "DoubleDoubles",
            "TripleDoubles",
            "FieldGoalsAttempted2Share",
            "FieldGoalsAttempted3Share",
            "FreeThrowsAttemptedShare",
            "FieldGoalsMade2Share",
            "FieldGoalsMade3Share",
            "FreeThrowsMadeShare",
            "PointsMade2Rate",
            "PointsMade3Rate",
            "PointsMadeFreeThrowsRate",
            "PointsAttempted2Rate",
            "PointsAttempted3Rate",
            "Age"
        ]
        available_phase_type_code = ["RS", "PO", "FF"]
        available_stat_mode = [
            "PerGame",
            "Accumulated",
            "PerMinute",
            "Per100Possesions",
            "PerGameReverse",
            "AccumulatedReverse"
        ]
        available_game_types = [
            "HomeGames",
            "AwayGames",
            "GamesWon",
            "GamesLost",
        ]

        raise_error(stat_category, "Stat category",
                    avaiable_stat_category, False)
        raise_error(
            statistic_mode, "Statistic Aggregation", available_stat_mode,
            False)
        raise_error(
            phase_type_code, "Phase type code", available_phase_type_code,
            True)
        raise_error(game_type, "Game type", available_game_types, True)

        params["category"] = stat_category
        params["phaseTypeCode"] = phase_type_code
        params["statisticMode"] = statistic_mode
        params["limit"] = top_n

        url_ = f"{self.url_v2}/stats/clubs/leaders"

        r = get_requests(url_, params=params)
        data = r.json()
        df = pd.json_normalize(data["data"])
        return df

    def get_team_stats_leaders_all_seasons(
        self,
        stat_category: str | None = None,
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in all seasons

        Args:

            stat_category (str): The stat category. See function
                `self.get_team_stats_leaders` for a list of available stats.

            top_n (int): The number of top N teams to return.
                Defaults to 200.

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
                - PerMinute
                - Per100Possesions
                - PerGameReverse
                - AccumulatedReverse
                Defaults to "PerGame".

            game_type (Optional[str], optional): The type of games to draw the
                top stats from. Available values:
                - HomeGames
                - AwayGames
                - GamesWon
                - GamesLost
                Defaults to None, meaning all games

        Returns:

            pd.DataFrame: A dataframe with the top leading teams and their
                stat
        """
        params = {"SeasonMode": "All"}
        df = self.get_team_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type
        )
        return df

    def get_team_stats_leaders_single_season(
        self,
        season: int,
        stat_category: str = "Score",
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in a single season

        Args:

            season (int): The start year of the season.

            stat_category (str): The stat category. See function
                `self.get_team_stats_leaders` for a list of available stats.
            top_n (int): The number of top N teams to return.
                Defaults to 200.

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
                - PerMinute
                - Per100Possesions
                - PerGameReverse
                - AccumulatedReverse
                Defaults to "PerGame".

            game_type (Optional[str], optional): The type of games to draw the
                top stats from. Available values:
                - HomeGames
                - AwayGames
                - GamesWon
                - GamesLost
                Defaults to None, meaning all games

        Returns:

            pd.DataFrame: A dataframe with the top leading teams and their
                stat
        """
        params = {
            "SeasonMode": "Single",
            "SeasonCode": f"{self.competition}{season}",
        }
        df = self.get_team_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type
        )
        return df

    def get_team_stats_leaders_range_seasons(
        self,
        start_season: int,
        end_season: int,
        stat_category: str = "Score",
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in a range of seasons

        Args:

            start_season (int): The start year of the first season in the
                range.

            end_season (int): The end year of the last season in the range.

            stat_category (str): The stat category. See function
                `self.get_team_stats_leaders` for a list of available stats.

            top_n (int): The number of top N teams to return.
                Defaults to 200.

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
                - PerMinute
                - Per100Possesions
                - PerGameReverse
                - AccumulatedReverse
                Defaults to "PerGame".

            game_type (Optional[str], optional): The type of games to draw the
                top stats from. Available values:
                - HomeGames
                - AwayGames
                - GamesWon
                - GamesLost
                Defaults to None, meaning all games

        Returns:

            pd.DataFrame: A dataframe with the top leading teams and their
                stat
        """
        params = {
            "SeasonMode": "Range",
            "FromSeasonCode": f"{self.competition}{start_season}",
            "ToSeasonCode": f"{self.competition}{end_season}",
        }
        df = self.get_team_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type
        )
        return df
