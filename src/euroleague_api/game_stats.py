import pandas as pd
from .utils import get_season_data_from_game_data
from .utils import get_range_seasons_data
from .utils import get_game_data


def get_game_report(season: int, game_code: int) -> pd.DataFrame:
    """
    Get game report data for a game

    Args:
        season (int): The start year of the season
        game_code (int): The game code of the game of interest. It can be found
            on Euroleague's website.

    Returns:
        pd.DataFrame: A dataframw with the game report data
    """
    df = get_game_data(season, game_code, "report")
    return df


def get_game_reports_single_season(season: int) -> pd.DataFrame:
    """
    Get game report data for *all* games in a single season

    Args:
        season (int): The start year of the season

    Returns:
        pd.DataFrame: A dataframe with game report data
    """
    data_df = get_season_data_from_game_data(season, get_game_report)
    return data_df


def get_game_reports_range_seasons(
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
    df = get_range_seasons_data(start_season, end_season, get_game_report)
    return df


def get_game_stats(season: int, game_code: int) -> pd.DataFrame:
    """
    Get game stats data for single game

    Args:

        season (int): The start year of the season

        game_code (int): The game code of the game of interest. It can be found
            on Euroleague's website.

    Returns:

        pd.DataFrame: A dataframe with the games' stats data
    """
    df = get_game_data(season, game_code, "stats")
    return df


def get_game_stats_single_season(season: int) -> pd.DataFrame:
    """
    Get game stats data for *all* games in a single season

    Args:

        season (int): The start year of the season

    Returns:

        pd.DataFrame: A dataframe with the games' stats data
    """
    data_df = get_season_data_from_game_data(season, get_game_stats)
    return data_df


def get_game_stats_range_seasons(
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
    df = get_range_seasons_data(start_season, end_season, get_game_stats)
    return df


def get_game_teams_comparison(
    season: int,
    game_code: int
) -> pd.DataFrame:
    """
    A function that gets the "teams comparison" game stats for a single game

    Args:

        season (int): The start year of the season

        game_code (int): The game code of the game of interest. It can be found
            on Euroleague's website.

    Returns:

        pd.DataFrame: A dataframe with games teams comparison stats
    """
    df = get_game_data(season, game_code, "teamsComparison")
    return df


def get_game_teams_comparison_single_season(season: int) -> pd.DataFrame:
    """
    A function that gets the "teams comparison" game stats for *all* games
    in a single season

    Args:

        season (int): The start year of the season

    Returns:

        pd.DataFrame: A dataframe with games teams comparison stats
    """
    data_df = get_season_data_from_game_data(
        season, get_game_teams_comparison)
    return data_df


def get_game_teams_comparison_range_seasons(
    start_season: int,
    end_season: int
) -> pd.DataFrame:
    """
    A function that gets the "teams comparison" game stats for *all* in a
    range seasons

    Args:

        start_season (int): The start year of the star season

        end_season (int): The start year of the end season

    Returns:

        pd.DataFrame: A dataframe with games teams comparison stats
    """
    df = get_range_seasons_data(
        start_season,
        end_season,
        get_game_teams_comparison
    )
    return df
