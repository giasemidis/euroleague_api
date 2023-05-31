from typing import Optional
from utils import get_player_stats
import pandas as pd


def get_player_stats_leaders_all_seasons(
    endpoint: str,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = "PerGame"
) -> pd.DataFrame:
    """"""
    params = {"SeasonMode": "All"}
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df


def get_player_stats_leaders_single_season(
    endpoint: str,
    season: int,
    phase_type_code: str,
    statistic_mode: str
) -> pd.DataFrame:
    """"""
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
    """"""
    params = {
        "SeasonMode": "Range",
        "FromSeasonCode": f"E{from_season}",
        "ToSeasonCode": f"E{to_season}",
    }
    df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)
    return df
