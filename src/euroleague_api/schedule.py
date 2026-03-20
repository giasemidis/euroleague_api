import pandas as pd
from .EuroLeagueData import EuroLeagueData
from .utils import get_requests


class Standings(EuroLeagueData):
    """"""

    def get_schedule(self, season: int) -> pd.DataFrame:
        """"""
        url = f"{self.BASE_URL}/{self.V1}/schedules?seasonCode={self.competition}{season}"
        r = get_requests(url)
        schedule_dict = xmltodict.parse(r.text)
        df = pd.DataFrame(schedule_dict["schedule"]["item"])
        df["gameday"] = df["gameday"].astype(int)
        return df
