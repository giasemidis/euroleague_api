from typing import Dict, Union, Callable, Optional
import logging
import requests
import pandas as pd

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_URL = "https://api-live.euroleague.net"
version = "v3"
competition = "E"
URL = f"{BASE_URL}/{version}/competitions/{competition}"


def make_season_game_url(
    season_code: int,
    game_code: int,
    endpoint: str
) -> str:
    """
    Concatenates the base URL and makes the game url.

    Args:
        season_code (int): The start year of the season
        game_code (int): The code of the game. Find the code from
            Euroleague's website
        endpoint (str): The endpoint of the API

    Returns:
        str: the full URL
    """
    FULL_URL = f"{URL}/seasons/E{season_code}/games/{game_code}/{endpoint}"
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


def get_game_data(
    season_code: int,
    game_code: int,
    endpoint: str
) -> pd.DataFrame:
    """
    A wrapper function for getting game-level data.

    Args:
        season_code (int): The start year of the season
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
    if endpoint not in game_endpoints:
        raise ValueError(
            f"Game endpoint, {endpoint}, is not applicable. "
            f"Available endpoints {game_endpoints}"
        )

    url_ = make_season_game_url(season_code, game_code, endpoint)
    r = get_requests(url_)

    data = r.json()
    df = pd.json_normalize(data)
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
    game_code = 0
    attempt = 0
    while True:
        game_code += 1
        shots_df = fun(season, game_code)

        # Due to the ban of Russian teams from Euroleague in 2021
        # this is a hack for not breaking in the first
        # "empty" game, but only after 5 *concecutive*
        # "empty" games
        if shots_df is None:
            attempt += 1
        else:
            attempt = 0
            data_list.append(shots_df)

        if attempt > 5:
            logger.debug(
                "No more available game data for this season, break and exit"
            )
            break

    if data_list:
        data_df = pd.concat(data_list, axis=0)
    else:
        data_df = pd.DataFrame([])
    return data_df


def get_multiple_seasons_data(
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
    for season in range(start_season, end_season + 1):
        data_df = get_season_data_from_game_data(season, fun)
        data.append(data_df)
    df = pd.concat(data)
    return df


def get_player_stats(
    endpoint: str,
    params: Dict[str, Union[str, int]],
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
    available_stat_code = ["PerGame", "Accumulated", "Per100Possesions"]

    if endpoint not in available_endpoints:
        raise ValueError(
            f"Statistic type, {endpoint}, is not applicable. "
            f"Available values: {available_endpoints}"
        )

    if phase_type_code is not None:
        if phase_type_code not in available_phase_type_code:
            raise ValueError(
                f"Phase type, {phase_type_code}, is not applicable. "
                f"Available values: {available_phase_type_code}"
            )
        params["phaseTypeCode"] = phase_type_code

    if statistic_mode not in available_stat_code:
        raise ValueError(
            f"Statistic mode, {statistic_mode}, is not applicable. "
            f"Available values: {available_stat_code}"
        )
    params["statisticMode"] = statistic_mode

    params["limit"] = 400

    url_ = f"{URL}/statistics/players/{endpoint}"

    r = get_requests(url_, params=params)
    data = r.json()
    if data["total"] < len(data["players"]):
        params["limit"] = len(data["players"]) + 1
        r = get_requests(url_, params=params)
        data = r.json()
    df = pd.json_normalize(data["players"])
    return df


def get_team_stats(
    endpoint: str,
    params: Dict[str, Union[str, int]],
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
    available_stat_code = ["PerGame", "Accumulated"]

    if endpoint not in available_endpoints:
        raise ValueError(
            f"Statistic type, {endpoint}, is not applicable. "
            f"Available values: {available_endpoints}"
        )

    if phase_type_code is not None:
        if phase_type_code not in available_phase_type_code:
            raise ValueError(
                f"Phase type, {phase_type_code}, is not applicable. "
                f"Available values: {available_phase_type_code}"
            )
        params["phaseTypeCode"] = phase_type_code

    if statistic_mode not in available_stat_code:
        raise ValueError(
            f"Statistic mode, {statistic_mode}, is not applicable. "
            f"Available values: {available_stat_code}"
        )
    params["statisticMode"] = statistic_mode

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
