# Module euroleague_api.play_by_play_data

## Variables

```python3
logger
```

## Classes

### PlayByPlay

```python3
class PlayByPlay(
    competition='E'
)
```

A class for getting the game play-by-play data.

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

    
#### get_game_play_by_play_data

```python3
def get_game_play_by_play_data(
    self,
    season: int,
    gamecode: int
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data of a particular game.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play data of the game. |

    
#### get_game_play_by_play_data_multiple_seasons

```python3
def get_game_play_by_play_data_multiple_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data of *all* games in a range of

seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play data of all games<br>in range of seasons |

    
#### get_game_play_by_play_data_single_season

```python3
def get_game_play_by_play_data_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data of *all* games in a single

season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play data of all games<br>in a single season |

    
#### get_pbp_data_with_lineups

```python3
def get_pbp_data_with_lineups(
    self,
    season,
    gamecode,
    validate=True
) -> pandas.core.frame.DataFrame
```

Get the play-by-play (PBP) data enriched with the teams' lineups for

every action in the PBP data.

There are three cases where the player in the corresponding row
(action) is not part of the lineup:

    1. When the player is subbed "OUT", the assigned lineup does not
    contain player name. Since this is reasonable, the value of the
    `validate_on_court_player` indicator is set to `True`.

    2. A player passes on to a teamate, who draws a shooting foul. If
    the passer is subbed before the first free throw and the first free
    throw is made then the subbed player is given an assist. However,
    the player is not in the extracted lineup because he has already
    been subbed. The value of the `validate_on_court_player`
    indicator is set to `False`. We don't fix the lineup, because it
    breaks the lineup continuinity. It is a quirk of the data
    collection andrecording.

    3. There are a few instances where a sub is recorded many seconds
    and actions since it actually happened. This causes issues, such
    as a player records an actions, such as a rebound, but he comes
    on the court (according to the data) many seconds after. This has
    been validated by watching theactual footage of the game. This
    requires a lot of manual work, which is beyond the score of this
    library. It is another quirk of the datacollection and recording,
    hence the value of the `validate_on_court_player` indicator is set
    to `False`.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| gamecode | int | The game-code of the game of interest.<br>It can be found on Euroleague's website. | None |
| validate | bool | A bool indicator whether to enrich the<br>dataframe with two extra columns, which validate the validity<br>and consistency of the extracted lineup. Defaults to True. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play enriched with<br>teams' lineups |

    
#### get_pbp_data_with_lineups_multiple_seasons

```python3
def get_pbp_data_with_lineups_multiple_seasons(
    self,
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data enriched with team lineups

of *all* games in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the start season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play data of all games<br>in range of seasons |

    
#### get_pbp_data_with_lineups_single_season

```python3
def get_pbp_data_with_lineups_single_season(
    self,
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the play-by-play data enriched with team lineups

of *all* games in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the play-by-play data of all games<br>in a single season |

    
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
