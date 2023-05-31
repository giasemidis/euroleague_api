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


def make_season_game_url(seasonCode: int, gameCode: int, endpoint: str) -> str:
    FULL_URL = f"{URL}/seasons/E{seasonCode}/games/{gameCode}/{endpoint}"
    return FULL_URL


def get_requests(url, params={}, headers={"Accept": "application/json"}):
    """
    """
    r = requests.get(
        url, params=params, headers={"Accept": "application/json"})

    if r.status_code != 200:
        raise ValueError()

    return r


def get_game_data(
    seasonCode: int,
    gameCode: int,
    endpoint: str
) -> pd.DataFrame:
    url_ = make_season_game_url(seasonCode, gameCode, endpoint)
    r = get_requests(url_)

    data = r.json()
    df = pd.json_normalize(data)
    return df


def get_season_data_from_game_data(
    season: int,
    fun: Callable[[int, int], pd.DataFrame]
) -> pd.DataFrame:
    """_summary_

    Args:
        season (int, optional): _description_. Defaults to 2022.

    Returns:
        Optional[pd.DataFrame]: _description_
    """
    data_list = []
    gamecode = 0
    attempt = 0
    while True:
        gamecode += 1
        shots_df = fun(season, gamecode)

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
    """"""

    available_endpoints = ["traditional", "advanced", "misc", "scoring"]
    available_phase_type_code = ["RS", "PO", "FF"]
    available_stat_code = ["PerGame", "Accumulated", "Per100Possesions"]

    if endpoint not in available_endpoints:
        raise ValueError("endpoint")

    if phase_type_code is not None:
        if phase_type_code not in available_phase_type_code:
            raise ValueError("phaseTypeCode")
        params["phaseTypeCode"] = phase_type_code

    if statistic_mode not in available_stat_code:
        raise ValueError("statisticMode")
    params["statisticMode"] = statistic_mode

    params["limit"] = 400

    url_ = f"{URL}/{endpoint}"
    r = get_requests(url_, params=params)
    data = r.json()
    if data["total"] < len(data["players"]):
        params["limit"] = len(data["players"]) + 1
        r = get_requests(url_, params=params)
        data = r.json()
    df = pd.json_normalize(data["players"])
    return df
