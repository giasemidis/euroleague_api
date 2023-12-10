# Module euroleague_api.game_stats

??? example "View Source"
        import pandas as pd

        from .utils import get_season_data_from_game_data

        from .utils import get_range_seasons_data

        from .utils import get_game_data

        

        def get_game_report(season: int, game_code: int) -> pd.DataFrame:

            """

            Get game report data for a game

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframw with the game report data

            """

            df = get_game_data(season, game_code, "report")

            return df

        

        def get_game_reports_single_season(season: int) -> pd.DataFrame:

            """

            Get game report data for *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with game report data

            """

            data_df = get_season_data_from_game_data(season, get_game_report)

            return data_df

        

        def get_game_reports_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            Get game report data for *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with game report data

            """

            df = get_range_seasons_data(start_season, end_season, get_game_report)

            return df

        

        def get_game_stats(season: int, game_code: int) -> pd.DataFrame:

            """

            Get game stats data for single game

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            df = get_game_data(season, game_code, "stats")

            return df

        

        def get_game_stats_single_season(season: int) -> pd.DataFrame:

            """

            Get game stats data for *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            data_df = get_season_data_from_game_data(season, get_game_stats)

            return data_df

        

        def get_game_stats_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            Get game stats data for *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            df = get_range_seasons_data(start_season, end_season, get_game_stats)

            return df

        

        def get_game_teams_comparison(

            season: int,

            game_code: int

        ) -> pd.DataFrame:

            """

            A function that gets the "teams comparison" game stats for a single game.

            This is the *pre-game* stats. Hence gamecodes of round 1 of each season are

            not available.

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            df = get_game_data(season, game_code, "teamsComparison")

            return df

        

        def get_game_teams_comparison_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the pre-grame "teams comparison" game stats for *all*

            games in a single season.

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            data_df = get_season_data_from_game_data(

                season, get_game_teams_comparison)

            return data_df

        

        def get_game_teams_comparison_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the pre-game "teams comparison" game stats for *all*

            in a range seasons

            Args:

                start_season (int): The start year of the star season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            df = get_range_seasons_data(

                start_season,

                end_season,

                get_game_teams_comparison

            )

            return df

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

??? example "View Source"
        def get_game_report(season: int, game_code: int) -> pd.DataFrame:

            """

            Get game report data for a game

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframw with the game report data

            """

            df = get_game_data(season, game_code, "report")

            return df

    
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

??? example "View Source"
        def get_game_reports_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            Get game report data for *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with game report data

            """

            df = get_range_seasons_data(start_season, end_season, get_game_report)

            return df

    
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

??? example "View Source"
        def get_game_reports_single_season(season: int) -> pd.DataFrame:

            """

            Get game report data for *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with game report data

            """

            data_df = get_season_data_from_game_data(season, get_game_report)

            return data_df

    
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

??? example "View Source"
        def get_game_stats(season: int, game_code: int) -> pd.DataFrame:

            """

            Get game stats data for single game

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            df = get_game_data(season, game_code, "stats")

            return df

    
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

??? example "View Source"
        def get_game_stats_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            Get game stats data for *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            df = get_range_seasons_data(start_season, end_season, get_game_stats)

            return df

    
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

??? example "View Source"
        def get_game_stats_single_season(season: int) -> pd.DataFrame:

            """

            Get game stats data for *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the games' stats data

            """

            data_df = get_season_data_from_game_data(season, get_game_stats)

            return data_df

    
### get_game_teams_comparison

```python3
def get_game_teams_comparison(
    season: int,
    game_code: int
) -> pandas.core.frame.DataFrame
```

A function that gets the "teams comparison" game stats for a single game.

This is the *pre-game* stats. Hence gamecodes of round 1 of each season are
not available.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |
| game_code | int | The game code of the game of interest. It can be found<br>on Euroleague's website. | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

??? example "View Source"
        def get_game_teams_comparison(

            season: int,

            game_code: int

        ) -> pd.DataFrame:

            """

            A function that gets the "teams comparison" game stats for a single game.

            This is the *pre-game* stats. Hence gamecodes of round 1 of each season are

            not available.

            Args:

                season (int): The start year of the season

                game_code (int): The game code of the game of interest. It can be found

                    on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            df = get_game_data(season, game_code, "teamsComparison")

            return df

    
### get_game_teams_comparison_range_seasons

```python3
def get_game_teams_comparison_range_seasons(
    start_season: int,
    end_season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the pre-game "teams comparison" game stats for *all*

in a range seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| start_season | int | The start year of the star season | None |
| end_season | int | The start year of the end season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

??? example "View Source"
        def get_game_teams_comparison_range_seasons(

            start_season: int,

            end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the pre-game "teams comparison" game stats for *all*

            in a range seasons

            Args:

                start_season (int): The start year of the star season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            df = get_range_seasons_data(

                start_season,

                end_season,

                get_game_teams_comparison

            )

            return df

    
### get_game_teams_comparison_single_season

```python3
def get_game_teams_comparison_single_season(
    season: int
) -> pandas.core.frame.DataFrame
```

A function that gets the pre-grame "teams comparison" game stats for *all*

games in a single season.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| season | int | The start year of the season | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with games teams comparison stats |

??? example "View Source"
        def get_game_teams_comparison_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the pre-grame "teams comparison" game stats for *all*

            games in a single season.

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with games teams comparison stats

            """

            data_df = get_season_data_from_game_data(

                season, get_game_teams_comparison)

            return data_df