from typing import Optional, List
import requests


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
