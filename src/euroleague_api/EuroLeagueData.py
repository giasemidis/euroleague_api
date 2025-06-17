from typing import Callable
import logging
from json.decoder import JSONDecodeError
import pandas as pd
from tqdm.auto import trange
import xmltodict
from .utils import get_requests, get_data_over_collection_of_games

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
    V3 = "v3"
    V2 = "v2"
    V1 = "v1"

    def __init__(self, competition="E"):
        """init function for the EuroLeagueData class.

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
        self.url_v1 = f"{self.BASE_URL}/{self.V1}/results/"
        self.url_v2 = f"{self.BASE_URL}/{self.V2}/competitions/{competition}"
        # Don't rename url to url_v3, as the former it's used is several places
        self.url = f"{self.BASE_URL}/{self.V3}/competitions/{competition}"

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

    def get_gamecodes_season(self, season: int) -> pd.DataFrame:
        """
        A function that returns the game metadata, e.g. gamecodes of season

        Args:

            season (int): The start year of the season.

        Returns:

            pd.DataFrame: A dataframe with the season's game metadata, e.g.
                gamecode, score, home-away teams, date, round, etc.
        """
        params = {
            "seasonCode": f"{self.competition}{season}",
        }
        r = get_requests(self.url_v1, params=params)

        data = xmltodict.parse(r.content)
        df = pd.DataFrame(data["results"]["game"])
        df.rename(
            columns={
                "gamenumber": "gameCode",
                "round": "Phase",
                "gameday": "Round"
            },
            inplace=True
        )
        int_cols = ["Round", "gameCode", "homescore", "awayscore"]
        df[int_cols] = df[int_cols].astype(int)
        df["played"] = df["played"].astype(
            bool).replace({"true": True, "false": False})
        df.sort_values(["gameCode"], ignore_index=True, inplace=True)
        return df

    def get_gamecodes_round(
            self, season: int,
            round_number: int
    ) -> pd.DataFrame:
        """
        A function that returns the game metadata, e.g. gamecodes of a round
        in a season.

        Args:

            season (int): The start year of the season.

            round_number (int): The round number.

        Returns:

            pd.DataFrame: A dataframe with the round_number's game metadata,
                e.g. gamecode, score, home-away teams, date, etc.
        """
        url = f"{self.url_v2}/seasons/{self.competition}{season}/games"
        params = {"roundNumber": round_number}
        r = get_requests(url, params=params)
        try:
            data = r.json()
        except JSONDecodeError as exc:
            raise ValueError(
                f"Round, {round_number}, season {season}, "
                "did not return any data."
            ) from exc

        df = pd.json_normalize(data["data"])
        df.rename(
            columns={
                "round": "Round",
                "phaseType.code": "Phase"
            },
            inplace=True
        )
        df.sort_values(["gameCode"], ignore_index=True, inplace=True)
        return df

    def get_round_data_from_game_data(
        self,
        season: int,
        round_number: int,
        fun: Callable[[int, int], pd.DataFrame]
    ) -> pd.DataFrame:
        """A wrapper function for getting game data for all games in a single
        round.

        Args:
            season (int, optional): The start year of the season.

            round_number (int): The round of the season.

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
            pd.DataFrame: A dataframe with the corresponding data of a single
                round
        """
        game_codes_df = self.get_gamecodes_round(season, round_number)
        game_codes_df = game_codes_df[game_codes_df["played"]]
        df = get_data_over_collection_of_games(
            game_codes_df,
            season=season,
            fun=fun
        )
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
                - get_game_play_by_play_data
                - get_game_shot_data
                - get_game_boxscore_quarter_data
                - get_player_boxscore_stats_data
                - get_game_metadata

        Returns:

            pd.DataFrame: A dataframe with the corresponding data of all
                games in a single season.
        """
        game_codes_df = self.get_gamecodes_season(season)
        game_codes_df = game_codes_df[game_codes_df["played"]]
        season_game_codes_df = (
            game_codes_df[["Phase", "Round", "gameCode"]]
            .drop_duplicates().sort_values(["gameCode", "Round"])
            .reset_index(drop=True)
        )
        df = get_data_over_collection_of_games(
            season_game_codes_df,
            season=season,
            fun=fun
        )
        return df

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
                - get_game_play_by_play_data
                - get_game_shot_data
                - get_game_boxscore_quarter_data
                - get_player_boxscore_stats_data
                - get_game_metadata

        Returns:

            pd.DataFrame: A dataframe with the corresponding data of all
                games in a range of seasons.
        """
        data = []
        for season in trange(
                start_season, end_season + 1, desc="Season loop", leave=True):

            data_df = self.get_season_data_from_game_data(season, fun)
            data.append(data_df)
        df = pd.concat(data)
        df.reset_index(drop=True, inplace=True)
        return df
