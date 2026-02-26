# Module euroleague_api.shot_data

## Variables

```python3
logger
```

## Classes

### ShotData

```python3
class ShotData(
    competition='E'
)
```

A class for getting shot data.

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

    
#### get_game_shot_data

```python3
def get_game_shot_data(
    self,
    season: int,
    gamecode: int
) -> pandas.core.frame.DataFrame
```

A function that gets the shot data of a particular game.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the shot data of the game. |

    
#### get_game_shot_data_range_seasons

```python3
def get_game_shot_data_range_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the shot data of *all* games in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the shot data of all games in range<br>of seasons |

    
#### get_game_shot_data_round

```python3
def get_game_shot_data_round(
    self,
    season: int,
    round_number: int
) -> pandas.core.frame.DataFrame
```

A function that gets the shot data of *all* games in a single round

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| round_number | int | The round of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the shot data of all games in a<br>single round |

    
#### get_game_shot_data_single_season

```python3
def get_game_shot_data_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the shot data of *all* games in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the shot data of all games in a<br>single season |

    
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
