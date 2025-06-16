from typing import Optional, List, Callable
import requests
from requests.exceptions import HTTPError
import logging
import pandas as pd
from tqdm.auto import tqdm

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_requests(
    url: str,
    params: dict = {},
    headers: dict = {"Accept": "application/json"}
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
    r = requests.get(url, params=params, headers=headers, timeout=60)

    if r.status_code != 200:
        r.raise_for_status()

    return r


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


def get_data_over_collection_of_games(
    game_codes_df,
    season: int,
    fun: Callable[[int, int], pd.DataFrame]
) -> pd.DataFrame:
    """A function that collects data over a collection of games given their
    game codes. It is a wrapper function that calls the `fun` function

    Args:
        game_codes_df (_type_): _description_
        season (int, optional): The start year of the season.
        fun (Callable[[int, int], pd.DataFrame]): A callable function that
            determines that type of data to be collected. Available values:
            - get_game_report
            - get_game_stats
            - get_game_teams_comparison
            - get_game_play_by_play_data
            - get_game_shot_data
            - get_game_boxscore_quarter_data
            - get_player_boxscore_stats_data
            - get_game_metadata


    Returns:
        pd.DataFrame: A dataframe with the corresponding data of all
            games in the collection.
    """
    data_list = []
    for _, row in tqdm(game_codes_df.iterrows(),
                       total=game_codes_df.shape[0],
                       desc=f"Season {season}", leave=True):
        game_code = row["gameCode"]
        try:
            df = fun(season, game_code)
            if df.empty:
                logger.warning(
                    f"Game {game_code}, season {season} returned no data."
                )
                continue
            if ("Phase" not in df.columns) and ("Phase" in row):
                df.insert(1, "Phase", row["Phase"])
            if ("Round" not in df.columns) and ("Round" in row):
                df.insert(2, "Round", row["Round"])
            data_list.append(df)
        except HTTPError as err:
            logger.warning(
                f"HTTPError: Didn't find gamecode {game_code} for season "
                f"{season}. Invalid {err}. Skip and continue."
            )
        except Exception as e:  # noqa: E722
            logger.warning(
                f"\nSomething went wrong for game {game_code}, "
                f"season {season}.\nError message: {e}. "
                "\nSkip and continue"
            )

    if data_list:
        data_df = pd.concat(data_list, axis=0)
        data_df.reset_index(drop=True, inplace=True)
    else:
        data_df = pd.DataFrame([])
    return data_df
