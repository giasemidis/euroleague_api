from typing import Callable, Optional, List
import logging
import requests
from json.decoder import JSONDecodeError
import pandas as pd
import xmltodict
from tqdm.auto import tqdm, trange
from requests.exceptions import HTTPError

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_URL = "https://api-live.euroleague.net"
version = "v3"
competition = "E"
URL = f"{BASE_URL}/{version}/competitions/{competition}"


def make_season_game_url(
    season: int,
    game_code: int,
    endpoint: str
) -> str:
    """
    Concatenates the base URL and makes the game url.

    Args:

        season (int): The start year of the season

        game_code (int): The code of the game. Find the code from
            Euroleague's website

        endpoint (str): The endpoint of the API

    Returns:

        str: the full URL
    """
    FULL_URL = f"{URL}/seasons/E{season}/games/{game_code}/{endpoint}"
    return FULL_URL


def get_requests(
    url: str,
    params={},
    headers={"Accept": "application/json"}
) -> requests.models.Response:
    """
    A wrapper to `requests.get()` which handles unsuccesful requests too.

    Args:

        url (str): _description_

        params (dict, optional): The `params` variables in get requests.
            Defaults to {}.

        headers (dict, optional): the `header` variable in get requests.
            Defaults to {"Accept": "application/json"}.

    Raises:

        Requests Error: If get request was not succesful

    Returns:

        requests.models.Response: The response object.
    """
    r = requests.get(url, params=params, headers=headers)

    if r.status_code != 200:
        r.raise_for_status()

    return r


def get_game_data(season: int, game_code: int, endpoint: str) -> pd.DataFrame:
    """
    A wrapper function for getting game-level data.

    Args:

        season (int): The start year of the season

        game_code (int): The game code of the game of interest.
            Find the game code from Euroleague's website

        endpoint (str): The type of game data, available variables:
            - report
            - stats
            - teamsComparison

    Raises:

        ValueError: If input endpoint is not applicable.

    Returns:

        pd.DataFrame: A dataframe with the game data.
    """
    game_endpoints = ["report", "stats", "teamsComparison"]

    raise_error(endpoint, "Statistic type", game_endpoints, False)

    url_ = make_season_game_url(season, game_code, endpoint)
    r = get_requests(url_)

    data = r.json()
    df = pd.json_normalize(data)
    df.insert(0, "Season", season)
    if "gameCode" in df.columns:
        df.rename(columns={"gameCode": "Gamecode"}, inplace=True)
    else:
        df.insert(1, "Gamecode", game_code)
    if "round" in df.columns:
        df.rename(columns={"round": "Round"}, inplace=True)

    return df


def get_game_metadata_season(season: int) -> pd.DataFrame:
    """
    A function that returns the game metadata, e.g. gamecodes of season

    Args:

        season (int): The start year of the season.

    Returns:

        pd.DataFrame: A dataframe with the season's game metadata, e.g.
            gamecode, score, home-away teams, date, round, etc.
    """
    url = f"https://api-live.euroleague.net/v1/results?seasonCode=E{season}"
    r = get_requests(url)
    data = xmltodict.parse(r.content)
    df = pd.DataFrame(data["results"]["game"])
    int_cols = ["gameday", "gamenumber", "homescore", "awayscore"]
    df[int_cols] = df[int_cols].astype(int)
    df["played"] = df["played"].replace({"true": True, "false": False})
    return df


def get_season_data_from_game_data(
    season: int,
    fun: Callable[[int, int], pd.DataFrame]
) -> pd.DataFrame:
    """
    A wrapper function for getting game data for all games in a single season.

    Args:

        season (int, optional): The start year of the season.

        fun (Callable[[int, int], pd.DataFrame]): A callable function that
            determines that type of data to be collected. Available values:
            - get_game_report
            - get_game_stats
            - get_game_teams_comparison

    Returns:

        pd.DataFrame: A dataframe with the game data.
    """
    data_list = []

    game_metadata_df = get_game_metadata_season(season)
    game_metadata_df = game_metadata_df[game_metadata_df["played"]]
    game_codes_df = (
        game_metadata_df[["round", "gameday", "gamenumber"]]
        .drop_duplicates().sort_values(["gamenumber", "gameday"])
        .reset_index(drop=True)
    )
    for _, row in tqdm(game_codes_df.iterrows(), total=game_codes_df.shape[0],
                       desc=f"Season {season}", leave=True):
        game_code = row["gamenumber"]
        try:
            df = fun(season, game_code)
            if df.empty:
                logger.warning(f"Game {game_code} returned no data.")
                continue
            if ("Phase" not in df.columns) and ("round" in row):
                df.insert(1, "Phase", row["round"])
            if ("Round" not in df.columns) and ("gameday" in row):
                df.insert(2, "Round", row["gameday"])
            data_list.append(df)
        except HTTPError as err:
            logger.warning(
                f"HTTPError: Didn't find gamecode {game_code} for season "
                f"{season}. Invalid {err}. Skip and continue."
            )
        except:  # noqa: E722
            logger.warning(
                f"Something went wrong for game {game_code}. Skip and continue"
            )

    if data_list:
        data_df = pd.concat(data_list, axis=0)
        data_df.reset_index(drop=True, inplace=True)
    else:
        data_df = pd.DataFrame([])
    return data_df


def get_range_seasons_data(
    start_season: int,
    end_season: int,
    fun: Callable[[int, int], pd.DataFrame]
) -> pd.DataFrame:
    """
    A wrapper function with the all game data in a range of seasons

    Args:

        season (int, optional): The start year of the season.

        end_season (int): The start year of teh end season

        fun (Callable[[int, int], pd.DataFrame]): A callable function that
            determines that type of data to be collected. Available values:
            - get_game_report
            - get_game_stats
            - get_game_teams_comparison

    Returns:

        pd.DataFrame: A dataframe with the game data
    """
    data = []
    for season in trange(
            start_season, end_season + 1, desc="Season loop", leave=True):

        data_df = get_season_data_from_game_data(season, fun)
        data.append(data_df)
    df = pd.concat(data)
    df.reset_index(drop=True, inplace=True)
    return df


def get_player_stats(
    endpoint: str,
    params={},
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

        params (Dict[str, Union[str, int]]): A dictionary of parameters for the
            get request.

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
        statistic_mode, "Statistic Aggregation", available_stat_mode, False)
    raise_error(
        phase_type_code, "Phase type code", available_phase_type_code, True)

    params["statisticMode"] = statistic_mode
    params["phaseTypeCode"] = phase_type_code
    params["limit"] = 400

    url_ = f"{URL}/statistics/players/{endpoint}"

    r = get_requests(url_, params=params)
    data = r.json()
    if data["total"] > len(data["players"]):
        params["limit"] = data["total"] + 1
        r = get_requests(url_, params=params)
        data = r.json()
    df = pd.json_normalize(data["players"])
    return df


def get_team_stats(
    endpoint: str,
    params={},
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

        params (Dict[str, Union[str, int]]): A dictionary of the parmaters for
            the get request.

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
        statistic_mode, "Statistic Aggregation", available_stat_mode, False)
    raise_error(
        phase_type_code, "Phase type code", available_phase_type_code, True)

    params["statisticMode"] = statistic_mode
    params["phaseTypeCode"] = phase_type_code
    params["limit"] = 400

    url_ = f"{URL}/statistics/teams/{endpoint}"

    r = get_requests(url_, params=params)
    data = r.json()
    if data["total"] < len(data["teams"]):
        params["limit"] = len(data["teams"]) + 1
        r = get_requests(url_, params=params)
        data = r.json()
    df = pd.json_normalize(data["teams"])
    return df


def get_player_stats_leaders(
    params={},
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

        params (Dict[str, Union[str, int]]): A dictionary of parameters for the
            get request.

        top_n (int): The number of top N players to return.  Defaults to 200.

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

    raise_error(stat_category, "Stat category", avaiable_stat_category, False)
    raise_error(
        statistic_mode, "Statistic Aggregation", available_stat_mode, False)
    raise_error(
        phase_type_code, "Phase type code", available_phase_type_code, True)
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

    url_ = f"{URL}/stats/players/leaders"

    r = get_requests(url_, params=params)
    data = r.json()
    df = pd.json_normalize(data["data"])
    return df


def raise_error(
    var: Optional[str],
    descripitve_var: str,
    available_vals: List,
    allow_none: bool = False,
) -> None:
    """
    A function that raises a ValueError with specific message.

    Args:

        var (str): The input variable by the user

        descripitve_var (str): A description in plain English of this variable

        available_vals (List): The available variables

        allow_none (bool, optional): If `var` can take None value.
            Defaults to False.

    Raises:

        ValueError: if `var` not applicable
    """

    if allow_none:
        available_vals.append(None)

    if var not in available_vals:
        raise ValueError(
            f"{descripitve_var}, {var}, is not applicable. "
            f"Available values: {available_vals}"
        )
    return


def get_boxscore_data(
    season: int,
    gamecode: int,
    boxscore_type: str = "ByQuarter"
) -> List[dict]:
    """A helper function that gets the boxscore data of a particular data.

    Args:
        season (int): The start year of the season
        gamecode (int): The game-code of the game of interest.
            It can be found on Euroleague's website.
        boxscore_type (str, optional): The type of quarter boxscore data.
            Available values:
            - Stats
            - ByQuarter
            - EndOfQuarter
            Defaults to "ByQuarter".

    Raises:
        ValueError: If boxscore_type value is not valid.

    Returns:
        List[dict]: A list of dictionaries with the data.
    """
    url = "https://live.euroleague.net/api/Boxscore"
    params = {
        "gamecode": gamecode,
        "seasoncode": f"E{season}"
    }
    r = get_requests(url, params=params)

    try:
        data = r.json()
    except JSONDecodeError:
        raise ValueError(f"Game code, {gamecode}, did not return any data.")
    boxscore_types = ["Stats", "ByQuarter", "EndOfQuarter"]

    if boxscore_type not in boxscore_types:
        raise_error(boxscore_type, "Boxscore", boxscore_types, False)

    return data[boxscore_type]
