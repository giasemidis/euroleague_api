# Module euroleague_api.utils

## Variables

```python3
logger
```

## Functions

    
### get_data_over_collection_of_games

```python3
def get_data_over_collection_of_games(
    game_codes_df,
    season: int,
    fun: Callable[[int, int], pandas.core.frame.DataFrame]
) -> pandas.core.frame.DataFrame
```

A function that collects data over a collection of games given their

game codes. It is a wrapper function that calls the `fun` function

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| game_codes_df | pd.DataFrame | A dataframe of the game codes to collect | None |
| season | int | The start year of the season. | None |
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison<br>- get_game_play_by_play_data<br>- get_game_shot_data<br>- get_game_boxscore_quarter_data<br>- get_player_boxscore_stats_data<br>- get_game_metadata | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the corresponding data of all<br>games in the collection. |

    
### get_pbp_lineups

```python3
def get_pbp_lineups(
    pbp_df: pandas.core.frame.DataFrame,
    boxscore_df: pandas.core.frame.DataFrame,
    validate=True
) -> pandas.core.frame.DataFrame
```

A function that extracts the lineups from play-by-play data.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| pbp_df | pd.DataFrame | The play-by-play dataframe. | None |
| boxscore_df | pd.DataFrame | The boxscore dataframe. | None |
| validate | bool | If to validate if the on-court players | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the lineups. |

    
### get_requests

```python3
def get_requests(
    url: str,
    params: dict = {},
    headers: dict = {'Accept': 'application/json'}
) -> requests.models.Response
```

A wrapper to `requests.get()` which handles unsuccesful requests too.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| url | str | _description_ | None |
| params | dict | The `params` variables in get requests.<br>Defaults to {}. | None |
| headers | dict | the `header` variable in get requests.<br>Defaults to {"Accept": "application/json"}. | None |

**Returns:**

| Type | Description |
|---|---|
| requests.models.Response | The response object. |

**Raises:**

| Type | Description |
|---|---|
| Requests Error | If get request was not succesful |

    
### raise_error

```python3
def raise_error(
    var: Optional[str],
    descripitve_var: str,
    available_vals: List,
    allow_none: bool = False
) -> None
```

A function that raises a ValueError with specific message.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| var | str | The input variable by the user | None |
| descripitve_var | str | A description in plain English of this variable | None |
| available_vals | List | The available variables | None |
| allow_none | bool | If `var` can take None value.<br>Defaults to False. | None |

**Raises:**

| Type | Description |
|---|---|
| ValueError | if `var` not applicable |
