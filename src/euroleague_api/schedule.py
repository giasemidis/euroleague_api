import pandas as pd
import xmltodict
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class Schedule(EuroLeagueData):
    """
    A class for getting schedule data.

    Args:
        competition (str, optional): The competition code, inherited from the
            `EuroLeagueData` class. Choose one of:
            - 'E' for Euroleague
            - 'U' for Eurocup
            Defaults to "E".
    """

    def get_schedule(self, season: int) -> pd.DataFrame:
        """
        Get the schedule of a season. The schedule includes the date,
        time, and the teams playing in each game.

        The schedule gets updated as the season progresses.

        Args:

            season (int): The start year of the season

        Returns:

            pd.DataFrame: A dataframe with the schedule of the games
        """
        url = f"{self.BASE_URL}/{self.V1}/schedules"
        params = {
            "seasonCode": f"{self.competition}{season}"
        }
        r = get_requests(url, params=params)
        schedule_dict = xmltodict.parse(r.text)
        df = pd.DataFrame(schedule_dict["schedule"]["item"])
        df["gameday"] = df["gameday"].astype(int)
        return df
