import pandas as pd
from utils import (
    get_requests,
    URL
)


def get_standings(
    season: int,
    round_number: int,
    endpoint: str = "basicstandings",
) -> pd.DataFrame:
    """"""
    available_endpoints = [
        "calendarstandings", "streaks",
        "aheadbehind", "margins",
        "basicstandings"
    ]

    if endpoint not in available_endpoints:
        raise ValueError("endpoint")

    url_ = f"{URL}/seasons/E{season}/rounds/{round_number}/{endpoint}"
    r = get_requests(url_)
    data = r.json()
    df = pd.json_normalize(data["teams"])
    return df
