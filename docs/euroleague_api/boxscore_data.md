# Module euroleague_api.boxscore_data

## Classes

### BoxScoreData

```python3
class BoxScoreData(
    competition='E'
)
```

A class for getting box-score data

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

    
#### get_boxscore_data

```python3
def get_boxscore_data(
    self,
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

    
#### get_game_boxscore_quarter_data

```python3
def get_game_boxscore_quarter_data(
    self,
    season: int,
    gamecode: int,
    boxscore_type: str = 'ByQuarter'
) -> pandas.core.frame.DataFrame
```

A function that gets the boxscore quarterly data of a particular game.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |
| boxscore_type | str | The type of quarter boxscore data.<br>Available values:<br>- ByQuarter<br>- EndOfQuarter<br>Default: ByQuarter | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the boxscore quarter data of the<br>game. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If boxscore_type value is not valid. |

    
#### get_game_boxscore_quarter_data_multiple_seasons

```python3
def get_game_boxscore_quarter_data_multiple_seasons(
    self,
    start_season: int,
    end_season: int,
    boxscore_type: str = 'ByQuarter'
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data of *all* games in a range of

seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |
| boxscore_type | str | The type of quarter boxscore data.<br>Available values:<br>- ByQuarter<br>- EndOfQuarter<br>Default: ByQuarter | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the boxscore quarter data of all<br>games in range of seasons |

    
#### get_game_boxscore_quarter_data_single_season

```python3
def get_game_boxscore_quarter_data_single_season(
    self,
    season: int,
    boxscore_type: str = 'ByQuarter'
) -> pandas.core.frame.DataFrame
```

A function that gets the boxscore quarter data of *all* games in a

single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| boxscore_type | str | The type of quarter boxscore data. | None |
| Available values | None | - ByQuarter<br>- EndOfQuarter | None |
| Default | None | ByQuarter | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the boxscore quarter data of all<br>games in a single season |

    
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

    
#### get_player_boxscore_stats_data

```python3
def get_player_boxscore_stats_data(
    self,
    season: int,
    gamecode: int
) -> pandas.core.frame.DataFrame
```

The players' and team's total stats of a particular game.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with home and away team player stats |

    
#### get_player_boxscore_stats_multiple_seasons

```python3
def get_player_boxscore_stats_multiple_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that return the player boxscore stats for all games in

multiple season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with home and away team player stats for<br>a season |

    
#### get_player_boxscore_stats_single_season

```python3
def get_player_boxscore_stats_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that return the player boxscore stats for all games in a

single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the start season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with home and away team player stats for<br>a season |

    
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
