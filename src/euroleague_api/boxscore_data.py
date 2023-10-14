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


def get_player_boxscore_stats_data(
    season: int,
    gamecode: int
) -> pd.DataFrame:
    """
    The players' and team's total stats of a particular game.

    Args:
        season (int): The start year of the season
        gamecode (int): The game-code of the game of interest.
            It can be found on Euroleague's website.

    Returns:
        pd.DataFrame: A dataframe with home and away team player stats
    """
    data = get_boxscore_data(season, gamecode, "Stats")
    home_df = pd.concat([
        pd.json_normalize(data[0]["PlayersStats"]),
        pd.json_normalize(data[0]["tmr"]),
        pd.json_normalize(data[0]["totr"])
    ])
    home_df.reset_index(drop=True, inplace=True)
    home_df.iloc[-2:, 0] = ["Team", "Total"]  # type: ignore
    home_df.iloc[-2:, 5] = ["Team", "Total"]  # type: ignore
    home_df["Team"] = home_df["Team"].fillna(method="ffill")
    home_df.insert(0, 'Season', season)
    home_df.insert(1, 'Gamecode', gamecode)
    home_df.insert(2, "Home", 1)

    away_df = pd.concat([
        pd.json_normalize(data[1]["PlayersStats"]),
        pd.json_normalize(data[1]["tmr"]),
        pd.json_normalize(data[1]["totr"])
    ])
    away_df.reset_index(drop=True, inplace=True)
    away_df.iloc[-2:, 0] = ["Team", "Total"]  # type: ignore
    away_df.iloc[-2:, 5] = ["Team", "Total"]  # type: ignore
    away_df["Team"] = away_df["Team"].fillna(method="ffill")
    away_df.insert(0, 'Season', season)
    away_df.insert(1, 'Gamecode', gamecode)
    away_df.insert(2, "Home", 0)

    df = pd.concat([home_df, away_df], axis=0)
    return df


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
    get_game_boxscore_quarter_data_ = (
        lambda season, gamecode: get_game_boxscore_quarter_data(
            season, gamecode, boxscore_type)
    )
    data_df = get_season_data_from_game_data(
        season, get_game_boxscore_quarter_data_)
    return data_df


def get_game_boxscore_quarter_data_multiple_seasons(
    start_season: int, end_season: int, boxscore_type: str = "ByQuarter"
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
    get_game_boxscore_quarter_data_ = (
        lambda season, gamecode: get_game_boxscore_quarter_data(
            season, gamecode, boxscore_type)
    )
    df = get_range_seasons_data(
        start_season, end_season, get_game_boxscore_quarter_data_)
    return df


def get_player_boxscore_stats_single_season(season: int) -> pd.DataFrame:
    """
    A function that return the player boxscore stats for all games in a
    single season

    Args:
        season (int): The start year of the start season

    Returns:
        pd.DataFrame: A dataframe with home and away team player stats for a
            season
    """
    data_df = get_season_data_from_game_data(
        season, get_player_boxscore_stats_data)
    return data_df


def get_player_boxscore_stats_multiple_seasons(
    start_season: int,
    end_season: int
) -> pd.DataFrame:
    """
    A function that return the player boxscore stats for all games in
    multiple season

    Args:
        start_season (int): The start year of the start season

        end_season (int): The start year of the end season

    Returns:
        pd.DataFrame: A dataframe with home and away team player stats for a
            season
    """
    data_df = get_range_seasons_data(
        start_season, end_season, get_player_boxscore_stats_data)
    return data_df
