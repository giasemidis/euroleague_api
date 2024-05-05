from typing import Callable
import logging
import pandas as pd
from tqdm.auto import tqdm, trange
from requests.exceptions import HTTPError
import xmltodict
from .utils import get_requests

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


class EuroLeagueData:
    """
    Base class for collecting Euroleague and Eurocup competition's data.

    Args:
        competition (str, optional): The competition code. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """
    BASE_URL = "https://api-live.euroleague.net"
    VERSION = "v3"

    def __init__(self, competition="E"):
        """_summary_

        Args:
            competition (str, optional): The competition code. Choose one of:
                - 'E' for Euroleague
                - 'U' for Eurocup
                Defaults to "E".

        Raises:
            ValueError: When an invalid competition code is provided.
        """
        if competition not in ["E", "U"]:
            raise ValueError(
                "Invalid competition value, {competition}. "
                "Valid values 'E', 'U'"
            )
        self.competition = competition
        self.url = f"{self.BASE_URL}/{self.VERSION}/competitions/{competition}"

    def make_season_game_url(
        self,
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
        full_url = (
            f"{self.url}/seasons/{self.competition}{season}/"
            f"games/{game_code}/{endpoint}"
        )
        return full_url

    def get_game_metadata_season(self, season: int) -> pd.DataFrame:
        """
        A function that returns the game metadata, e.g. gamecodes of season

        Args:

            season (int): The start year of the season.

        Returns:

            pd.DataFrame: A dataframe with the season's game metadata, e.g.
                gamecode, score, home-away teams, date, round, etc.
        """
        url = (
            "https://api-live.euroleague.net/v1/results"
            f"?seasonCode={self.competition}{season}"
        )
        r = get_requests(url)
        data = xmltodict.parse(r.content)
        df = pd.DataFrame(data["results"]["game"])
        int_cols = ["gameday", "gamenumber", "homescore", "awayscore"]
        df[int_cols] = df[int_cols].astype(int)
        df["played"] = df["played"].replace({"true": True, "false": False})
        return df

    def get_season_data_from_game_data(
        self,
        season: int,
        fun: Callable[[int, int], pd.DataFrame]
    ) -> pd.DataFrame:
        """
        A wrapper function for getting game data for all games in a single
        season.

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

        game_metadata_df = self.get_game_metadata_season(season)
        game_metadata_df = game_metadata_df[game_metadata_df["played"]]
        game_codes_df = (
            game_metadata_df[["round", "gameday", "gamenumber"]]
            .drop_duplicates().sort_values(["gamenumber", "gameday"])
            .reset_index(drop=True)
        )
        for _, row in tqdm(game_codes_df.iterrows(),
                           total=game_codes_df.shape[0],
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
                    f"Something went wrong for game {game_code}. "
                    "Skip and continue"
                )

        if data_list:
            data_df = pd.concat(data_list, axis=0)
            data_df.reset_index(drop=True, inplace=True)
        else:
            data_df = pd.DataFrame([])
        return data_df

    def get_range_seasons_data(
        self,
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

            data_df = self.get_season_data_from_game_data(season, fun)
            data.append(data_df)
        df = pd.concat(data)
        df.reset_index(drop=True, inplace=True)
        return df
