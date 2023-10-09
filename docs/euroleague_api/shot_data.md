# Module euroleague_api.shot_data

## Variables

```python3
MADE_ACTIONS
```

```python3
MISSES_ACTIONS
```

## Functions

    
### get_game_shot_data

```python3
def get_game_shot_data(
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

    
### get_game_shot_data_multiple_seasons

```python3
def get_game_shot_data_multiple_seasons(
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
| pd.DataFrame | A dataframe with the shot data of all games in range of<br>seasons |

    
### get_game_shot_data_single_season

```python3
def get_game_shot_data_single_season(
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
| pd.DataFrame | A dataframe with the shot data of all games in a single<br>season |
