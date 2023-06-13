from typing import Optional
import pandas as pd
from .utils import get_player_stats, get_player_stats_leaders


def get_player_stats_all_seasons(
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
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df


def get_player_stats_single_season(
    endpoint: str,
    season: int,
    phase_type_code: str,
    statistic_mode: str
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
        "SeasonCode": f"E{season}",
    }
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df


def get_player_stats_range_seasons(
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

        start_season (int): The start year of the first season in the range.

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
        "FromSeasonCode": f"E{start_season}",
        "ToSeasonCode": f"E{end_season}",
    }
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df


def get_player_stats_leaders_all_seasons(
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

        top_n (int): The number of top N players to return.  Defaults to 200.

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

        game_type (Optional[str], optional): The type of games to draw the top
            stats from. Available values:
            - HomeGames
            - AwayGames
            - GamesWon
            - GamesLost
            Defaults to None, meaning all games

        position (Optional[str], optional): The position of the player to draw
            the top stats from. Available values:
            - Guards
            - Forwards
            - Centers
            - RisingStars
            Defaults to None, meaning all positions.

    Returns:

        pd.DataFrame: A dataframe with the top leading players and their stat
    """
    params = {"SeasonMode": "All"}
    df = get_player_stats_leaders(
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
        top_n (int): The number of top N players to return.  Defaults to 200.

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

        game_type (Optional[str], optional): The type of games to draw the top
            stats from. Available values:
            - HomeGames
            - AwayGames
            - GamesWon
            - GamesLost
            Defaults to None, meaning all games

        position (Optional[str], optional): The position of the player to draw
            the top stats from. Available values:
            - Guards
            - Forwards
            - Centers
            - RisingStars
            Defaults to None, meaning all positions.

    Returns:

        pd.DataFrame: A dataframe with the top leading players and their stat
    """
    params = {
        "SeasonMode": "Single",
        "SeasonCode": f"E{season}",
    }
    df = get_player_stats_leaders(
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

        start_season (int): The start year of the first season in the range.

        stat_category (str): The stat category. See function
            `utils.get_player_stats_leaders` for a list of available stats.

        top_n (int): The number of top N players to return.  Defaults to 200.

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

        game_type (Optional[str], optional): The type of games to draw the top
            stats from. Available values:
            - HomeGames
            - AwayGames
            - GamesWon
            - GamesLost
            Defaults to None, meaning all games

        position (Optional[str], optional): The position of the player to draw
            the top stats from. Available values:
            - Guards
            - Forwards
            - Centers
            - RisingStars
            Defaults to None, meaning all positions.

    Returns:

        pd.DataFrame: A dataframe with the top leading players and their stat
    """
    params = {
        "SeasonMode": "Range",
        "FromSeasonCode": f"E{start_season}",
        "ToSeasonCode": f"E{end_season}",
    }
    df = get_player_stats_leaders(
        params,
        stat_category,
        top_n,
        phase_type_code,
        statistic_mode,
        game_type,
        position
    )
    return df
