# Module euroleague_api.player_stats

## Classes

### PlayerStats

```python3
class PlayerStats(
    competition='E'
)
```

A class for getting the player-level stats and data.

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

    
#### get_player_stats

```python3
def get_player_stats(
    self,
    endpoint: str,
    params: dict = {},
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
| params | Dict[str, Union[str, int]] | A dictionary of parameters<br>for the get request. | None |
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

    
#### get_player_stats_all_seasons

```python3
def get_player_stats_all_seasons(
    self,
    endpoint: str,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

The players' stats for *all* seasons.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats, available variables:<br>- traditional<br>- advanced<br>- misc<br>- scoring | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats |

    
#### get_player_stats_leaders

```python3
def get_player_stats_leaders(
    self,
    params: dict = {},
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
| params | Dict[str, Union[str, int]] | A dictionary of parameters<br>for the get request. | None |
| top_n | int | The number of top N players to return.<br>Defaults to 200. | None |
| stat_category | str | The stat category. Available values:<br>- Valuation<br>- Score<br>- TotalRebounds<br>- OffensiveRebounds<br>- Assistances<br>- Steals<br>- BlocksFavour<br>- BlocksAgainst<br>- Turnovers<br>- FoulsReceived<br>- FoulsCommited<br>- FreeThrowsMade<br>- FreeThrowsAttempted<br>- FreeThrowsPercent<br>- FieldGoalsMade2<br>- FieldGoalsAttempted2<br>- FieldGoals2Percent<br>- FieldGoalsMade3<br>- FieldGoalsAttempted3<br>- FieldGoals3Percent<br>- FieldGoalsMadeTotal<br>- FieldGoalsAttemptedTotal<br>- FieldGoalsPercent<br>- AccuracyMade<br>- AccuracyAttempted<br>- AccuracyPercent<br>- AssitancesTurnoversRation<br>- GamesPlayed<br>- GamesStarted<br>- TimePlayed<br>- Contras<br>- Dunks<br>- OffensiveReboundPercentage<br>- DefensiveReboundPercentage<br>- ReboundPercentage<br>- EffectiveFeildGoalPercentage<br>- TrueShootingPercentage<br>- AssistRatio<br>- TurnoverRatio<br>- FieldGoals2AttemptedRatio<br>- FieldGoals3AttemptedRatio<br>- FreeThrowRate<br>- Possessions<br>- GamesWon<br>- GamesLost<br>- DoubleDoubles<br>- TripleDoubles<br>- FieldGoalsAttempted2Share<br>- FieldGoalsAttempted3Share<br>- FreeThrowsAttemptedShare<br>- FieldGoalsMade2Share<br>- FieldGoalsMade3Share<br>- FreeThrowsMadeShare<br>- PointsMade2Rate<br>- PointsMade3Rate<br>- PointsMadeFreeThrowsRate<br>- PointsAttempted2Rate<br>- PointsAttempted3Rate<br>- Age | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the<br>top stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to<br>draw the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

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

    
#### get_player_stats_leaders_all_seasons

```python3
def get_player_stats_leaders_all_seasons(
    self,
    stat_category: str,
    top_n: int = 200,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame',
    game_type: Optional[str] = None,
    position: Optional[str] = None
) -> pandas.core.frame.DataFrame
```

Get the top leaders in a statistical category in all seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| stat_category | str | The stat category. See function<br>`utils.get_player_stats_leaders` for a list of available stats. | None |
| top_n | int | The number of top N players to return.<br>Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the<br>top stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to<br>draw the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their<br>stat |

    
#### get_player_stats_leaders_range_seasons

```python3
def get_player_stats_leaders_range_seasons(
    self,
    start_season: int,
    end_season: int,
    stat_category: str,
    top_n: int = 200,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame',
    game_type: Optional[str] = None,
    position: Optional[str] = None
) -> pandas.core.frame.DataFrame
```

Get the top leaders in a statistical category in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the first season in the<br>range. | None |
| stat_category | str | The stat category. See function<br>`utils.get_player_stats_leaders` for a list of available stats. | None |
| top_n | int | The number of top N players to return.<br>Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the<br>top stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to<br>draw the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their<br>stat |

    
#### get_player_stats_leaders_single_season

```python3
def get_player_stats_leaders_single_season(
    self,
    season: int,
    stat_category: str,
    top_n: int = 200,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame',
    game_type: Optional[str] = None,
    position: Optional[str] = None
) -> pandas.core.frame.DataFrame
```

Get the top leaders in a statistical category in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season. | None |
| stat_category | str | The stat category. See function<br>`utils.get_player_stats_leaders` for a list of available stats. | None |
| top_n | int | The number of top N players to return.<br>Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the<br>top stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to<br>draw the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their<br>stat |

    
#### get_player_stats_range_seasons

```python3
def get_player_stats_range_seasons(
    self,
    endpoint: str,
    start_season: int,
    end_season: int,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

The players' stats for a range of seasons.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats, available variables:<br>- traditional<br>- advanced<br>- misc<br>- scoring | None |
| start_season | int | The start year of the first season in the<br>range. | None |
| end_season | int | The start year of teh last season in the range. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats |

    
#### get_player_stats_single_season

```python3
def get_player_stats_single_season(
    self,
    endpoint: str,
    season: int,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

The players' stats for a *single* season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats, available variables:<br>- traditional<br>- advanced<br>- misc<br>- scoring | None |
| season | int | The start year of the season. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats |

    
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
