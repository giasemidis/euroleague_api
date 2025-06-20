# Module euroleague_api.standings

## Classes

### Standings

```python3
class Standings(
    competition='E'
)
```

A class for getting standings data.

#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| competition | str | The competition code, inherited from the<br>`EuroLeagueData` class. Choose one of:<br>- 'E' for Euroleague<br>- 'U' for Eurocup<br>Defaults to "E". | None |

#### Ancestors (in MRO)

* euroleague_api.EuroLeagueData.EuroLeagueData

#### Class variables

```python3
BASE_URL
```

```python3
V1
```

```python3
V2
```

```python3
V3
```

#### Methods

    
#### get_gamecodes_round

```python3
def get_gamecodes_round(
    self,
    season: int,
    round_number: int
) -> pandas.core.frame.DataFrame
```

A function that returns the game metadata, e.g. gamecodes of a round

in a season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| round_number | int | The round number. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the round_number's game metadata,<br>e.g. gamecode, score, home-away teams, date, etc. |

    
#### get_gamecodes_season

```python3
def get_gamecodes_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that returns the game metadata, e.g. gamecodes of season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the season's game metadata, e.g.<br>gamecode, score, home-away teams, date, round, etc. |

    
#### get_range_seasons_data

```python3
def get_range_seasons_data(
    self,
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
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison<br>- get_game_play_by_play_data<br>- get_game_shot_data<br>- get_game_boxscore_quarter_data<br>- get_player_boxscore_stats_data<br>- get_game_metadata | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the corresponding data of all<br>games in a range of seasons. |

    
#### get_round_data_from_game_data

```python3
def get_round_data_from_game_data(
    self,
    season: int,
    round_number: int,
    fun: Callable[[int, int], pandas.core.frame.DataFrame]
) -> pandas.core.frame.DataFrame
```

A wrapper function for getting game data for all games in a single

round.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| round_number | int | The round of the season. | None |
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison<br>- get_game_play_by_play_data<br>- get_game_shot_data<br>- get_game_boxscore_quarter_data<br>- get_player_boxscore_stats_data<br>- get_game_metadata | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the corresponding data of a single<br>round |

    
#### get_season_data_from_game_data

```python3
def get_season_data_from_game_data(
    self,
    season: int,
    fun: Callable[[int, int], pandas.core.frame.DataFrame]
) -> pandas.core.frame.DataFrame
```

A wrapper function for getting game data for all games in a single

season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison<br>- get_game_play_by_play_data<br>- get_game_shot_data<br>- get_game_boxscore_quarter_data<br>- get_player_boxscore_stats_data<br>- get_game_metadata | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the corresponding data of all<br>games in a single season. |

    
#### get_standings

```python3
def get_standings(
    self,
    season: int,
    round_number: int,
    endpoint: str = 'basicstandings'
) -> pandas.core.frame.DataFrame
```

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

    
#### make_season_game_url

```python3
def make_season_game_url(
    self,
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
