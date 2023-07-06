from typing import Tuple
import pandas as pd
from .utils import raise_error
from .utils import get_boxscore_data
from .utils import get_season_data_from_game_data
from .utils import get_range_seasons_data


def get_game_boxscore_quarter_data(
        season: int,
        gamecode: int,
        boxscore_type: str = "ByQuarter"
) -> pd.DataFrame:
    """
    A function that gets the boxscore quarterly data of a particular game.

    Args:

        season (int): The start year of the season

        gamecode (int): The game-code of the game of interest.
            It can be found on Euroleague's website.

        boxscore_type (str): The type of quarter boxscore data.
            Available values:
            - ByQuarter
            - EndOfQuarter
            Default: ByQuarter

    Raises:
        ValueError: If boxscore_type value is not valid.

    Returns:

        pd.DataFrame: A dataframe with the boxscore quarter data of the game.
    """
    valid_vals = ["ByQuarter", "EndOfQuarter"]
    if boxscore_type not in valid_vals:
        raise_error(boxscore_type, "Boxscore quarter type", valid_vals, False)

    data = get_boxscore_data(season, gamecode, boxscore_type)
    df = pd.json_normalize(data)
    df.insert(0, 'Season', season)
    df.insert(1, 'Gamecode', gamecode)
    return df


def get_game_boxscore_stats_data(
    season: int,
    gamecode: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    The players' and team's total stats of a particular game.

    Args:
        season (int): The start year of the season
        gamecode (int): The game-code of the game of interest.
            It can be found on Euroleague's website.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple of dataframes of the player
            stats.
            First element is the home-team players' stats dataframe
            Second element is the away-team players' stats dataframe
    """
    data = get_boxscore_data(season, gamecode, "Stats")
    home_df = pd.concat([
        pd.json_normalize(data["Stats"][0]["PlayersStats"]),
        pd.json_normalize(data["Stats"][0]["tmr"]),
        pd.json_normalize(data["Stats"][0]["totr"])
    ])
    home_df.reset_index(drop=True, inplace=True)
    home_df.iloc[-2:, 0] = ["Team", "Total"]
    home_df.iloc[-2:, 5] = ["Team", "Total"]
    home_df["Team"] = home_df["Team"].fillna(method="ffill")
    home_df.insert(0, 'Season', season)
    home_df.insert(1, 'Gamecode', gamecode)

    away_df = pd.concat([
        pd.json_normalize(data["Stats"][1]["PlayersStats"]),
        pd.json_normalize(data["Stats"][1]["tmr"]),
        pd.json_normalize(data["Stats"][1]["totr"])
    ])
    away_df.reset_index(drop=True, inplace=True)
    away_df.iloc[-2:, 0] = ["Team", "Total"]
    away_df.iloc[-2:, 5] = ["Team", "Total"]
    away_df["Team"] = away_df["Team"].fillna(method="ffill")
    away_df.insert(0, 'Season', season)
    away_df.insert(1, 'Gamecode', gamecode)
    return home_df, away_df


def get_game_boxscore_quarter_data_single_season(
    season: int,
    boxscore_type: str = "ByQuarter"
) -> pd.DataFrame:
    """
    A function that gets the boxscore quarter data of *all* games in a single
    season

    Args:

        season (int): The start year of the season

        boxscore_type (str): The type of quarter boxscore data.
        Available values:
            - ByQuarter
            - EndOfQuarter
        Default: ByQuarter

    Returns:

        pd.DataFrame: A dataframe with the boxscore quarter data of all games
            in a single season
    """
    data_df = get_season_data_from_game_data(
        season, get_game_boxscore_quarter_data)
    return data_df


def get_game_boxscore_quarter_data_multiple_seasons(
    start_season: int, end_season: int
) -> pd.DataFrame:
    """
    A function that gets the play-by-play data of *all* games in a range of
    seasons

    Args:

        start_season (int): The start year of the start season

        end_season (int): The start year of the end season

        boxscore_type (str): The type of quarter boxscore data.
            Available values:
            - ByQuarter
            - EndOfQuarter
            Default: ByQuarter

    Returns:

        pd.DataFrame: A dataframe with the boxscore quarter data of all games
            in range of seasons
    """
    df = get_range_seasons_data(
        start_season, end_season, get_game_boxscore_quarter_data)
    return df
