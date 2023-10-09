# Module euroleague_api.game_stats

## Functions

    
### get_game_report

```python3
def get_game_report(
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

Get game report data for a game

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be found<br>on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframw with the game report data |

    
### get_game_reports_range_seasons

```python3
def get_game_reports_range_seasons(
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

    
### get_game_reports_single_season

```python3
def get_game_reports_single_season(
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

    
### get_game_stats

```python3
def get_game_stats(
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

Get game stats data for single game

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be found<br>on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the games' stats data |

    
### get_game_stats_range_seasons

```python3
def get_game_stats_range_seasons(
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

    
### get_game_stats_single_season

```python3
def get_game_stats_single_season(
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

    
### get_game_teams_comparison

```python3
def get_game_teams_comparison(
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

A function that gets the "teams comparison" game stats for a single game

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be found<br>on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

    
### get_game_teams_comparison_range_seasons

```python3
def get_game_teams_comparison_range_seasons(
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the "teams comparison" game stats for *all* in a

range seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the star season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

    
### get_game_teams_comparison_single_season

```python3
def get_game_teams_comparison_single_season(
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the "teams comparison" game stats for *all* games

in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |
