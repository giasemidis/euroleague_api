# Module euroleague_api.play_by_play_data

## Functions

    
### get_game_play_by_play_data

```python3
def get_game_play_by_play_data(
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

    
### get_game_shot_data_multiple_seasons

```python3
def get_game_shot_data_multiple_seasons(
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

    
### get_game_shot_data_single_season

```python3
def get_game_shot_data_single_season(
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
| pd.DataFrame | A dataframe with the play-by-play data of all games in a<br>single season |
