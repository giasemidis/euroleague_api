# Module euroleague_api.player_stats

??? example "View Source"
        from typing import Optional

        import pandas as pd

        from .utils import get_player_stats, get_player_stats_leaders

        

        def get_player_stats_all_seasons(

            endpoint: str,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            The players' stats for *all* seasons.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {"SeasonMode": "All"}

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

        

        def get_player_stats_single_season(

            endpoint: str,

            season: int,

            phase_type_code: str,

            statistic_mode: str

        ) -> pd.DataFrame:

            """

            The players' stats for a *single* season.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                season (int): The start year of the season.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                     - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

        

        def get_player_stats_range_seasons(

            endpoint: str,

            start_season: int,

            end_season: int,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            The players' stats for a range of seasons.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                start_season (int): The start year of the first season in the range.

                end_season (int): The start year of teh last season in the range.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                     - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{start_season}",

                "ToSeasonCode": f"E{end_season}",

            }

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

        

        def get_player_stats_leaders_all_seasons(

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in all seasons

            Args:

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {"SeasonMode": "All"}

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

        

        def get_player_stats_leaders_single_season(

            season: int,

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in a single season

            Args:

                season (int): The start year of the season.

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

        

        def get_player_stats_leaders_range_seasons(

            start_season: int,

            end_season: int,

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in a range of seasons

            Args:

                start_season (int): The start year of the first season in the range.

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{start_season}",

                "ToSeasonCode": f"E{end_season}",

            }

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

## Functions

    
### get_player_stats_all_seasons

```python3
def get_player_stats_all_seasons(
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

??? example "View Source"
        def get_player_stats_all_seasons(

            endpoint: str,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            The players' stats for *all* seasons.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {"SeasonMode": "All"}

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

    
### get_player_stats_leaders_all_seasons

```python3
def get_player_stats_leaders_all_seasons(
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
| top_n | int | The number of top N players to return.  Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the top<br>stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to draw<br>the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their stat |

??? example "View Source"
        def get_player_stats_leaders_all_seasons(

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in all seasons

            Args:

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {"SeasonMode": "All"}

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

    
### get_player_stats_leaders_range_seasons

```python3
def get_player_stats_leaders_range_seasons(
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
| start_season | int | The start year of the first season in the range. | None |
| stat_category | str | The stat category. See function<br>`utils.get_player_stats_leaders` for a list of available stats. | None |
| top_n | int | The number of top N players to return.  Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the top<br>stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to draw<br>the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their stat |

??? example "View Source"
        def get_player_stats_leaders_range_seasons(

            start_season: int,

            end_season: int,

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in a range of seasons

            Args:

                start_season (int): The start year of the first season in the range.

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{start_season}",

                "ToSeasonCode": f"E{end_season}",

            }

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

    
### get_player_stats_leaders_single_season

```python3
def get_player_stats_leaders_single_season(
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
| top_n | int | The number of top N players to return.  Defaults to 200. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>- Per100Possesions<br>- PerGameReverse<br>- AccumulatedReverse<br>Defaults to "PerGame". | None |
| game_type | Optional[str] | The type of games to draw the top<br>stats from. Available values:<br>- HomeGames<br>- AwayGames<br>- GamesWon<br>- GamesLost<br>Defaults to None, meaning all games | None |
| position | Optional[str] | The position of the player to draw<br>the top stats from. Available values:<br>- Guards<br>- Forwards<br>- Centers<br>- RisingStars<br>Defaults to None, meaning all positions. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the top leading players and their stat |

??? example "View Source"
        def get_player_stats_leaders_single_season(

            season: int,

            stat_category: str,

            top_n: int = 200,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame",

            game_type: Optional[str] = None,

            position: Optional[str] = None

        ) -> pd.DataFrame:

            """

            Get the top leaders in a statistical category in a single season

            Args:

                season (int): The start year of the season.

                stat_category (str): The stat category. See function

                    `utils.get_player_stats_leaders` for a list of available stats.

                top_n (int): The number of top N players to return.  Defaults to 200.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                    - PerGame

                    - Accumulated

                    - Per100Possesions

                    - PerGameReverse

                    - AccumulatedReverse

                    Defaults to "PerGame".

                game_type (Optional[str], optional): The type of games to draw the top

                    stats from. Available values:

                    - HomeGames

                    - AwayGames

                    - GamesWon

                    - GamesLost

                    Defaults to None, meaning all games

                position (Optional[str], optional): The position of the player to draw

                    the top stats from. Available values:

                    - Guards

                    - Forwards

                    - Centers

                    - RisingStars

                    Defaults to None, meaning all positions.

            Returns:

                pd.DataFrame: A dataframe with the top leading players and their stat

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_player_stats_leaders(

                params,

                stat_category,

                top_n,

                phase_type_code,

                statistic_mode,

                game_type,

                position

            )

            return df

    
### get_player_stats_range_seasons

```python3
def get_player_stats_range_seasons(
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
| start_season | int | The start year of the first season in the range. | None |
| end_season | int | The start year of teh last season in the range. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br> - PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats |

??? example "View Source"
        def get_player_stats_range_seasons(

            endpoint: str,

            start_season: int,

            end_season: int,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            The players' stats for a range of seasons.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                start_season (int): The start year of the first season in the range.

                end_season (int): The start year of teh last season in the range.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                     - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{start_season}",

                "ToSeasonCode": f"E{end_season}",

            }

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

    
### get_player_stats_single_season

```python3
def get_player_stats_single_season(
    endpoint: str,
    season: int,
    phase_type_code: str,
    statistic_mode: str
) -> pandas.core.frame.DataFrame
```

The players' stats for a *single* season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats, available variables:<br>- traditional<br>- advanced<br>- misc<br>- scoring | None |
| season | int | The start year of the season. | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br> - PerGame<br>- Accumulated<br>- Per100Possesions<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the players' stats |

??? example "View Source"
        def get_player_stats_single_season(

            endpoint: str,

            season: int,

            phase_type_code: str,

            statistic_mode: str

        ) -> pd.DataFrame:

            """

            The players' stats for a *single* season.

            Args:

                endpoint (str): The type of stats, available variables:

                    - traditional

                    - advanced

                    - misc

                    - scoring

                season (int): The start year of the season.

                phase_type_code (Optional[str], optional): The phase of the season,

                    available variables:

                    - "RS" (regular season)

                    - "PO" (play-off)

                    - "FF" (final four)

                    Defaults to None, which includes all phases.

                statistic_mode (str, optional): The aggregation of statistics,

                    available variables:

                     - PerGame

                    - Accumulated

                    - Per100Possesions

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the players' stats

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_player_stats(endpoint, params, phase_type_code, statistic_mode)

            return df