import pandas as pd
from utils import get_season_data_from_game_data
from utils import get_multiple_seasons_data
from utils import get_game_data


def get_game_report(seasonCode: int, gameCode: int) -> pd.DataFrame:
    df = get_game_data(seasonCode, gameCode, "report")
    return df


def get_game_reports_single_season(season: int):
    """
    """
    data_df = get_season_data_from_game_data(season, get_game_report)
    return data_df


def get_game_reports_multiple_seasons(start_season: int, end_season: int):
    """
    """
    df = get_multiple_seasons_data(start_season, end_season, get_game_report)
    return df


def get_game_stats(seasonCode: int, gameCode: int) -> pd.DataFrame:
    df = get_game_data(seasonCode, gameCode, "stats")
    return df


def get_game_stats_single_season(season: int) -> pd.DataFrame:
    """
    """
    data_df = get_season_data_from_game_data(season, get_game_stats)
    return data_df


def get_game_stats_multiple_seasons(
    start_season: int,
    end_season: int
) -> pd.DataFrame:
    """
    """
    df = get_multiple_seasons_data(start_season, end_season, get_game_stats)
    return df


def get_game_teams_comparison(seasonCode: int, gameCode: int) -> pd.DataFrame:
    df = get_game_data(seasonCode, gameCode, "teamsComparison")
    return df


def get_game_teams_comparison_single_season(season: int) -> pd.DataFrame:
    """
    """
    data_df = get_season_data_from_game_data(
        season, get_game_teams_comparison)
    return data_df


def get_game_teams_comparison_multiple_seasons(
    start_season: int,
    end_season: int
) -> pd.DataFrame:
    """
    """
    df = get_multiple_seasons_data(
        start_season,
        end_season,
        get_game_teams_comparison
    )
    return df
