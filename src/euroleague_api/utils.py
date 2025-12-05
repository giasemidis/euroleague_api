from typing import Optional, List, Callable
import requests
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
import logging
import pandas as pd
import numpy as np
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
        game_codes_df (pd.DataFrame): A dataframe of the game codes to collect
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
            logger.error(
                f"HTTPError: Didn't find gamecode {game_code} for season "
                f"{season}. \nError message {err}. "
                "\nSkip and continue."
            )
        except JSONDecodeError:
            logger.error(
                f"JSONDecodeError: Game code, {game_code}, "
                f"season {season}, did not return valid JSON data. "
                "\nSkip and continue."
            )
        except Exception as e:  # noqa: E722
            logger.error(
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


def get_pbp_lineups(
    pbp_df: pd.DataFrame,
    boxscore_df: pd.DataFrame,
    validate=True,
) -> pd.DataFrame:
    """
    A function that extracts the lineups from play-by-play data.

    Args:

        pbp_df (pd.DataFrame): The play-by-play dataframe.
        boxscore_df (pd.DataFrame): The boxscore dataframe.
        validate (bool, optional): If to validate if the on-court players

    Returns:

        pd.DataFrame: A dataframe with the lineups.
    """

    def process_sub(five, player, sub_type):
        opp_sub_type = "OUT" if sub_type == "IN" else "IN"
        potential_indx = (
            pbp_df.loc[idx + 1:].index[
                (pbp_df.loc[idx + 1:, "PLAYTYPE"] == opp_sub_type)
            ]
        )
        potential_nops = (
            set(potential_indx).difference(processed_idxs)
        )
        if not potential_nops:
            logger.warning(
                f"No potential matching subs found for gamecode "
                f"{gamecode} and season {season}"
            )
            return five
        matching_idx = min(potential_nops)
        processed_idxs.append(idx)
        processed_idxs.append(matching_idx)
        matching_row = pbp_df.loc[matching_idx]
        invalid_mask = (
            (matching_row["PLAYTYPE"] != opp_sub_type) or
            (matching_row["CODETEAM"] != team) or
            (matching_row["MARKERTIME"] != markertime)
        )
        if invalid_mask:
            logger.warning(
                f"Something went wrong for gamecode {gamecode} at sub "
                f"index {idx} with matching sub index {matching_idx}"
            )
        player_sub = matching_row["PLAYER"]
        player_in = player if sub_type == "IN" else player_sub
        player_out = player_sub if sub_type == "IN" else player
        if player_in == player_out:
            # there are instance where the same player is subbed in and out
            return five
        elif player_out not in five:
            logger.warning(
                f"Player {player_out} not found in current lineup, "
                f"{five}, for gamecode {gamecode} and season {season}."
            )
            return five
        else:
            pindx = five.index(player_out)
            five = five[:pindx] + [player_in] + five[pindx + 1:]
            return five

    def validate_player(x, col1, col2):
        flag = False
        if (x["PLAYER"] is not None) and (x["PLAYTYPE"] != "OUT"):
            if x["PLAYER"] in (x[col1] + x[col2]):
                flag = True
        else:
            flag = True
        return flag

    if pbp_df.empty or (pbp_df is None):
        return pbp_df

    if boxscore_df.empty or (boxscore_df is None):
        pbp_df["validate_on_court_player"] = False
        pbp_df["Lineup_A"] = pbp_df["Lineup_A"].apply(lambda x: [])
        pbp_df["Lineup_B"] = pbp_df["Lineup_B"].apply(lambda x: [])
        return pbp_df

    pbp_df = pbp_df.copy()
    gamecodes = pbp_df["Gamecode"].unique()
    if len(gamecodes) > 1:
        raise ValueError(
            "PBP DataFrame contains multiple game codes. "
            "Please provide data for a single game."
        )
    seasons = pbp_df["Season"].unique()
    if len(seasons) > 1:
        raise ValueError(
            "PBP DataFrame contains multiple seasons. "
            "Please provide data for a single season."
        )
    gamecode = gamecodes[0]
    season = seasons[0]

    # Asign the starting lineups to the first entry of the PBP data.
    pbp_df["Lineup_A"] = None
    pbp_df["Lineup_B"] = None

    # find home and away teams
    hm_aw = boxscore_df[["Home", "Team"]].drop_duplicates()
    home_team = hm_aw.loc[hm_aw["Home"] == 1, "Team"].values[0]
    away_team = hm_aw.loc[hm_aw["Home"] == 0, "Team"].values[0]

    starting_five = boxscore_df.loc[
        boxscore_df["IsStarter"] == 1, ["Team", "Player"]
    ]
    starting_five['ID'] = starting_five.groupby('Team').cumcount()

    # Pivot the DataFrame
    starting_five = starting_five.pivot(
        index='ID', columns='Team', values='Player')

    # Reset index if needed
    starting_five.reset_index(drop=True, inplace=True)
    starting_five = starting_five[[home_team, away_team]]
    # TODO: remove cleaning, this has been done in boxscore data
    starting_five[home_team] = starting_five[home_team].str.replace(
        "  ", " ").str.replace(" , ", ", ").str.strip()
    starting_five[away_team] = starting_five[away_team].str.replace(
        "  ", " ").str.replace(" , ", ", ").str.strip()
    starting_five_dict = starting_five.to_dict(orient='list')

    pbp_df.at[0, "Lineup_A"] = starting_five_dict[home_team]
    pbp_df.at[0, "Lineup_B"] = starting_five_dict[away_team]
    if "IsHomeTeam" not in pbp_df.columns:
        pbp_df["IsHomeTeam"] = np.where(
            pbp_df["CODETEAM"] == home_team, True,
            np.where(pbp_df["CODETEAM"] == away_team,
                     False, None)  # type: ignore
        )
    # start processing the sub entries, row by row.
    processed_idxs: list = []
    current_five_home = starting_five_dict[home_team].copy()
    current_five_away = starting_five_dict[away_team].copy()
    for idx, row in pbp_df.iterrows():
        playtype = row["PLAYTYPE"]
        # there are rare instances of an extra space in player name
        player = (
            row["PLAYER"] if row["PLAYER"] is None
            else row["PLAYER"]
        )
        team = row["CODETEAM"]
        markertime = row["MARKERTIME"]
        if team != "":
            is_home = home_team == team
            five = current_five_home if is_home else current_five_away
            if (playtype == "OUT") and (idx not in processed_idxs):
                five = process_sub(five, player, playtype)
            elif (playtype == "IN") and (idx not in processed_idxs):
                five = process_sub(five, player, playtype)
            if is_home:
                current_five_home = five
            else:
                current_five_away = five

        pbp_df.at[idx, "Lineup_A"] = current_five_home
        pbp_df.at[idx, "Lineup_B"] = current_five_away

    if validate:
        lu_cols = [u for u in pbp_df.columns if u.startswith("Lineup_")]
        pbp_df["validate_on_court_player"] = pbp_df.apply(
            lambda x: validate_player(x, lu_cols[0], lu_cols[1]),
            axis=1
        )

    if "TRUE_NUMBEROFPLAY" in pbp_df.columns:
        pbp_df["TRUE_NUMBEROFPLAY"] = np.arange(pbp_df.shape[0])

    return pbp_df
