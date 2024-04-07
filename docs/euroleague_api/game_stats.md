# Module euroleague_api.game_stats

## Classes

### GameStats

```python3
class GameStats(
    competition='E'
)
```

A class for getting the game related stats and data.

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
VERSION
```

#### Methods

    
#### get_game_data

```python3
def get_game_data(
    self,
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

    
#### get_game_metadata_season

```python3
def get_game_metadata_season(
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

    
#### get_game_report

```python3
def get_game_report(
    self,
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

Get game report data for a game

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be<br>found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframw with the game report data |

    
#### get_game_reports_range_seasons

```python3
def get_game_reports_range_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

Get game report data for *all* games in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with game report data |

    
#### get_game_reports_single_season

```python3
def get_game_reports_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

Get game report data for *all* games in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with game report data |

    
#### get_game_stats

```python3
def get_game_stats(
    self,
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

Get game stats data for single game

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be<br>found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the games' stats data |

    
#### get_game_stats_range_seasons

```python3
def get_game_stats_range_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

Get game stats data for *all* games in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the games' stats data |

    
#### get_game_stats_single_season

```python3
def get_game_stats_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

Get game stats data for *all* games in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the games' stats data |

    
#### get_game_teams_comparison

```python3
def get_game_teams_comparison(
    self,
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

A function that gets the "teams comparison" game stats for a single

game. This is the *pre-game* stats. Hence gamecodes of round 1 of each
season are not available.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be<br>found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

    
#### get_game_teams_comparison_range_seasons

```python3
def get_game_teams_comparison_range_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the pre-game "teams comparison" game stats for

*all* in a range seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the star season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

    
#### get_game_teams_comparison_single_season

```python3
def get_game_teams_comparison_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the pre-grame "teams comparison" game stats for

*all* games in a single season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

    
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
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the game data |

    
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
| fun | Callable[[int, int], pd.DataFrame] | A callable function that<br>determines that type of data to be collected. Available values:<br>- get_game_report<br>- get_game_stats<br>- get_game_teams_comparison | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the game data. |

    
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
