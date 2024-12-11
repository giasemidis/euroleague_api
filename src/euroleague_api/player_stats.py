from typing import Optional
import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import (
    raise_error,
    get_requests
)


class PlayerStats(EuroLeagueData):
    """
    A class for getting the player-level stats and data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_player_stats(
        self,
        endpoint: str,
        params: dict = {},
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        A wrapper function for getting the players' stats for
        - all seasons
        - a single season
        - a range of seasons

        Args:

            endpoint (str): The type of stats, available variables:
                - traditional
                - advanced
                - misc
                - scoring

            params (Dict[str, Union[str, int]]): A dictionary of parameters
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
                - Per100Possesions
                Defaults to "PerGame".

        Raises:

            ValueError: If the endpoint is not applicable

            ValueError: If the phase_type_code is not applicable

            ValueError: If the statistic_mode is not applicable

        Returns:

            pd.DataFrame: A dataframe with the players' stats.
        """

        available_endpoints = ["traditional", "advanced", "misc", "scoring"]
        available_phase_type_code = ["RS", "PO", "FF"]
        available_stat_mode = ["PerGame", "Accumulated", "Per100Possesions"]

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

        url_ = f"{self.url}/statistics/players/{endpoint}"

        r = get_requests(url_, params=params)
        data = r.json()
        if data["total"] > len(data["players"]):
            params["limit"] = data["total"] + 1
            r = get_requests(url_, params=params)
            data = r.json()
        df = pd.json_normalize(data["players"])
        return df

    def get_player_stats_leaders(
        self,
        params: dict = {},
        stat_category: str = "Score",
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None,
        position: Optional[str] = None
    ) -> pd.DataFrame:
        """
        A wrapper function for collecting the leading players in a given
        stat category.

        Args:

            params (Dict[str, Union[str, int]]): A dictionary of parameters
                for the get request.

            top_n (int): The number of top N players to return.
                Defaults to 200.

            stat_category (str): The stat category. Available values:
                - Valuation
                - Score
                - TotalRebounds
                - OffensiveRebounds
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

            position (Optional[str], optional): The position of the player to
                draw the top stats from. Available values:
                - Guards
                - Forwards
                - Centers
                - RisingStars
                Defaults to None, meaning all positions.

        Raises:

            ValueError: If the stat_category is not applicable

            ValueError: If the phase_type_code is not applicable

            ValueError: If the statistic_mode is not applicable

            ValueError: If the game_type is not applicable

            ValueError: If the position is not applicable

        Returns:

            pd.DataFrame: A dataframe with the top players' stats
        """
        avaiable_stat_category = [
            "Valuation",
            "Score",
            "TotalRebounds",
            "OffensiveRebounds",
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
        availabe_positions = [
            "Guards",
            "Forwards",
            "Centers",
            "RisingStars"
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
        raise_error(position, "Position", availabe_positions, True)

        params["category"] = stat_category
        params["phaseTypeCode"] = phase_type_code
        params["statisticMode"] = statistic_mode
        params["limit"] = top_n
        if game_type is not None and position is not None:
            raise ValueError(
                "Cannot select a game_type and position at the same type. "
                "One of the variables must be None"
            )
        elif game_type is not None and position is None:
            params["misc"] = game_type
        elif game_type is None and position is not None:
            params["misc"] = position

        url_ = f"{self.url}/stats/players/leaders"

        r = get_requests(url_, params=params)
        data = r.json()
        df = pd.json_normalize(data["data"])
        return df

    def get_player_stats_all_seasons(
        self,
        endpoint: str,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        The players' stats for *all* seasons.

        Args:

            endpoint (str): The type of stats, available variables:
                - traditional
                - advanced
                - misc
                - scoring

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
                - Per100Possesions
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the players' stats
        """
        params = {"SeasonMode": "All"}
        df = self.get_player_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_player_stats_single_season(
        self,
        endpoint: str,
        season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        The players' stats for a *single* season.

        Args:

            endpoint (str): The type of stats, available variables:
                - traditional
                - advanced
                - misc
                - scoring

            season (int): The start year of the season.

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
                - Per100Possesions
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the players' stats
        """
        params = {
            "SeasonMode": "Single",
            "SeasonCode": f"{self.competition}{season}",
        }
        df = self.get_player_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_player_stats_range_seasons(
        self,
        endpoint: str,
        start_season: int,
        end_season: int,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame"
    ) -> pd.DataFrame:
        """
        The players' stats for a range of seasons.

        Args:

            endpoint (str): The type of stats, available variables:
                - traditional
                - advanced
                - misc
                - scoring

            start_season (int): The start year of the first season in the
                range.

            end_season (int): The start year of teh last season in the range.

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
                - Per100Possesions
                Defaults to "PerGame".

        Returns:

            pd.DataFrame: A dataframe with the players' stats
        """
        params = {
            "SeasonMode": "Range",
            "FromSeasonCode": f"{self.competition}{start_season}",
            "ToSeasonCode": f"{self.competition}{end_season}",
        }
        df = self.get_player_stats(
            endpoint, params, phase_type_code, statistic_mode)
        return df

    def get_player_stats_leaders_all_seasons(
        self,
        stat_category: str,
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None,
        position: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in all seasons

        Args:

            stat_category (str): The stat category. See function
                `utils.get_player_stats_leaders` for a list of available stats.

            top_n (int): The number of top N players to return.
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

            position (Optional[str], optional): The position of the player to
                draw the top stats from. Available values:
                - Guards
                - Forwards
                - Centers
                - RisingStars
                Defaults to None, meaning all positions.

        Returns:

            pd.DataFrame: A dataframe with the top leading players and their
                stat
        """
        params = {"SeasonMode": "All"}
        df = self.get_player_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type,
            position
        )
        return df

    def get_player_stats_leaders_single_season(
        self,
        season: int,
        stat_category: str,
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None,
        position: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in a single season

        Args:

            season (int): The start year of the season.

            stat_category (str): The stat category. See function
                `utils.get_player_stats_leaders` for a list of available stats.
            top_n (int): The number of top N players to return.
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

            position (Optional[str], optional): The position of the player to
                draw the top stats from. Available values:
                - Guards
                - Forwards
                - Centers
                - RisingStars
                Defaults to None, meaning all positions.

        Returns:

            pd.DataFrame: A dataframe with the top leading players and their
                stat
        """
        params = {
            "SeasonMode": "Single",
            "SeasonCode": f"{self.competition}{season}",
        }
        df = self.get_player_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type,
            position
        )
        return df

    def get_player_stats_leaders_range_seasons(
        self,
        start_season: int,
        end_season: int,
        stat_category: str,
        top_n: int = 200,
        phase_type_code: Optional[str] = None,
        statistic_mode: str = "PerGame",
        game_type: Optional[str] = None,
        position: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get the top leaders in a statistical category in a range of seasons

        Args:

            start_season (int): The start year of the first season in the
                range.

            stat_category (str): The stat category. See function
                `utils.get_player_stats_leaders` for a list of available stats.

            top_n (int): The number of top N players to return.
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

            position (Optional[str], optional): The position of the player to
                draw the top stats from. Available values:
                - Guards
                - Forwards
                - Centers
                - RisingStars
                Defaults to None, meaning all positions.

        Returns:

            pd.DataFrame: A dataframe with the top leading players and their
                stat
        """
        params = {
            "SeasonMode": "Range",
            "FromSeasonCode": f"{self.competition}{start_season}",
            "ToSeasonCode": f"{self.competition}{end_season}",
        }
        df = self.get_player_stats_leaders(
            params,
            stat_category,
            top_n,
            phase_type_code,
            statistic_mode,
            game_type,
            position
        )
        return df
