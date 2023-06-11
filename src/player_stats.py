from typing import Optional
from utils import get_player_stats
import pandas as pd


def get_player_stats_leaders_all_seasons(
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


def get_player_stats_leaders_single_season(
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


def get_player_stats_leaders_range_seasons(
    endpoint: str,
    from_season: int,
    to_season: int,
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
        from_season (int): The start year of the first season in the range.
        to_season (int): The start year of teh last season in the range.
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
        "FromSeasonCode": f"E{from_season}",
        "ToSeasonCode": f"E{to_season}",
    }
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df
