# Module euroleague_api.boxscore_data

## Functions

    
### get_game_boxscore_quarter_data

```python3
def get_game_boxscore_quarter_data(
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
| pd.DataFrame | A dataframe with the boxscore quarter data of the game. |

**Raises:**

| Type | Description |
|---|---|
| ValueError | If boxscore_type value is not valid. |

    
### get_game_boxscore_quarter_data_multiple_seasons

```python3
def get_game_boxscore_quarter_data_multiple_seasons(
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
| pd.DataFrame | A dataframe with the boxscore quarter data of all games<br>in range of seasons |

    
### get_game_boxscore_quarter_data_single_season

```python3
def get_game_boxscore_quarter_data_single_season(
    season: int,
    boxscore_type: str = 'ByQuarter'
) -> pandas.core.frame.DataFrame
```

A function that gets the boxscore quarter data of *all* games in a single

season

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
| pd.DataFrame | A dataframe with the boxscore quarter data of all games<br>in a single season |

    
### get_game_boxscore_stats_data

```python3
def get_game_boxscore_stats_data(
    season: int,
    gamecode: int
) -> Tuple[pandas.core.frame.DataFrame, pandas.core.frame.DataFrame]
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
| Tuple[pd.DataFrame, pd.DataFrame] | A tuple of dataframes of the player<br>stats.<br>First element is the home-team players' stats dataframe<br>Second element is the away-team players' stats dataframe |
