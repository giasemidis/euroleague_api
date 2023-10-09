# Module euroleague_api.utils

## Variables

```python3
BASE_URL
```

```python3
URL
```

```python3
competition
```

```python3
logger
```

```python3
version
```

## Functions

    
### get_boxscore_data

```python3
def get_boxscore_data(
    season: int,
    gamecode: int,
    boxscore_type: str = 'ByQuarter'
) -> List[dict]
```

A helper function that gets the boxscore data of a particular data.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |
| boxscore_type | str | The type of quarter boxscore data.<br>Available values:<br>- Stats<br>- ByQuarter<br>- EndOfQuarter<br>Defaults to "ByQuarter". | None |

**Returns:**

| Type | Description |
|---|---|
| List[dict] | A list of dictionaries with the data. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If boxscore_type value is not valid. |

    
### get_game_data

```python3
def get_game_data(
    season: int,
    game_code: int,
    endpoint: str
) -> pandas.core.frame.DataFrame
```

A wrapper function for getting game-level data.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest.<br>Find the game code from Euroleague's website | None |
| endpoint | str | The type of game data, available variables:<br>- report<br>- stats<br>- teamsComparison | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the game data. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If input endpoint is not applicable. |

    
### get_player_stats

```python3
def get_player_stats(
    endpoint: str,
    params={},
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

A wrapper function for getting the players' stats for

- all seasons
- a single season
- a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats, available variables:<br>- traditional<br>- advanced<br>- misc<br>- scoring | None |
| params | Dict[str, Union[str, int]] | A dictionary of parameters for the<br>get request. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If the endpoint is not applicable |
| ValueError | If the phase_type_code is not applicable |
| ValueError | If the statistic_mode is not applicable |

    
### get_player_stats_leaders

```python3
def get_player_stats_leaders(
    params={},
    stat_category: str = 'Score',
    top_n: int = 200,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame',
    game_type: Optional[str] = None,
    position: Optional[str] = None
) -> pandas.core.frame.DataFrame
```

A wrapper function for collecting the leading players in a given

stat category.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | Dict[str, Union[str, int]] | A dictionary of parameters for the<br>get request. | None |
| top_n | int | The number of top N players to return.  Defaults to 200. | None |
| stat_category | str | The stat category. Available values:<br>- Valuation<br>- Score<br>- TotalRebounds<br>- OffensiveRebounds<br>- Assistances<br>- Steals<br>- BlocksFavour<br>- BlocksAgainst<br>- Turnovers<br>- FoulsReceived<br>- FoulsCommited<br>- FreeThrowsMade<br>- FreeThrowsAttempted<br>- FreeThrowsPercent<br>- FieldGoalsMade2<br>- FieldGoalsAttempted2<br>- FieldGoals2Percent<br>- FieldGoalsMade3<br>- FieldGoalsAttempted3<br>- FieldGoals3Percent<br>- FieldGoalsMadeTotal<br>- FieldGoalsAttemptedTotal<br>- FieldGoalsPercent<br>- AccuracyMade<br>- AccuracyAttempted<br>- AccuracyPercent<br>- AssitancesTurnoversRation<br>- GamesPlayed<br>- GamesStarted<br>- TimePlayed<br>- Contras<br>- Dunks<br>- OffensiveReboundPercentage<br>- DefensiveReboundPercentage<br>- ReboundPercentage<br>- EffectiveFeildGoalPercentage<br>- TrueShootingPercentage<br>- AssistRatio<br>- TurnoverRatio<br>- FieldGoals2AttemptedRatio<br>- FieldGoals3AttemptedRatio<br>- FreeThrowRate<br>- Possessions<br>- GamesWon<br>- GamesLost<br>- DoubleDoubles<br>- TripleDoubles<br>- FieldGoalsAttempted2Share<br>- FieldGoalsAttempted3Share<br>- FreeThrowsAttemptedShare<br>- FieldGoalsMade2Share<br>- FieldGoalsMade3Share<br>- FreeThrowsMadeShare<br>- PointsMade2Rate<br>- PointsMade3Rate<br>- PointsMadeFreeThrowsRate<br>- PointsAttempted2Rate<br>- PointsAttempted3Rate<br>- Age | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the top<br>stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to draw<br>the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top players' stats |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If the stat_category is not applicable |
| ValueError | If the phase_type_code is not applicable |
| ValueError | If the statistic_mode is not applicable |
| ValueError | If the game_type is not applicable |
| ValueError | If the position is not applicable |

    
### get_range_seasons_data

```python3
def get_range_seasons_data(
    start_season: int,
    end_season: int,
    fun: Callable[[int, int], pandas.core.frame.DataFrame]
) -> pandas.core.frame.DataFrame
```

A wrapper function with the all game data in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| end_season | int | The start year of teh end season | None |
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the game data |

    
### get_requests

```python3
def get_requests(
    url: str,
    params={},
    headers={'Accept': 'application/json'}
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

    
### get_season_data_from_game_data

```python3
def get_season_data_from_game_data(
    season: int,
    fun: Callable[[int, int], pandas.core.frame.DataFrame]
) -> pandas.core.frame.DataFrame
```

A wrapper function for getting game data for all games in a single season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the game data. |

    
### get_team_stats

```python3
def get_team_stats(
    endpoint: str,
    params={},
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

A wrapper functions for collecting teams' stats.

Allows for three types of data:
- all seasons
- single season
- range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats to fetch. Available values:<br>- traditional<br>- advanced<br>- opponentsTraditional<br>- opponentsAdvanced | None |
| params | Dict[str, Union[str, int]] | A dictionary of the parmaters for<br>the get request. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the teams' stats. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If the endpoint is not applicable |
| ValueError | If the phase_type_code is not applicable |
| ValueError | If the statistic_mode is not applicable |

    
### make_season_game_url

```python3
def make_season_game_url(
    season: int,
    game_code: int,
    endpoint: str
) -> str
```

Concatenates the base URL and makes the game url.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The code of the game. Find the code from<br>Euroleague's website | None |
| endpoint | str | The endpoint of the API | None |

**Returns:**

| Type | Description |
|---|---|
| str | the full URL |

    
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
