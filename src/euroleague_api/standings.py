import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class Standings(EuroLeagueData):
    """
    A class for getting standings data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_standings(
        self,
        season: int,
        round_number: int,
        endpoint: str = "basicstandings",
    ) -> pd.DataFrame:
        """
        Get the standings of round in given season

        Args:

            season (int): The start year of the season

            round_number (int): The round number

            endpoint (str, optional): The type of standing.
            One of the following options
            - calendarstandings
            - streaks
            - aheadbehind
            - margins
            - basicstandings
            Defaults to "basicstandings".

        Raises:

            ValueError: If endpoint is not applicable

        Returns:

            pd.DataFrame: A dataframe with the standings of the teams
        """
        available_endpoints = [
            "calendarstandings", "streaks",
            "aheadbehind", "margins",
            "basicstandings"
        ]

        if endpoint not in available_endpoints:
            raise ValueError(
                "Standings endpoint, {endpoint}, is not applicable. Choose "
                f"one of the following: {available_endpoints}"
            )

        url_ = (
            f"{self.url}/seasons/{self.competition}{season}/"
            f"rounds/{round_number}/{endpoint}"
        )
        r = get_requests(url_)
        data = r.json()
        df = pd.json_normalize(data["teams"])
        return df
