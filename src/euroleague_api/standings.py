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
    """Get the standings of round in given season

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
            "Standings endpoint, {endpoint}, is not applicable. Choose one of "
            f"the following: {available_endpoints}"
        )

    url_ = f"{URL}/seasons/E{season}/rounds/{round_number}/{endpoint}"
    r = get_requests(url_)
    data = r.json()
    df = pd.json_normalize(data["teams"])
    return df
