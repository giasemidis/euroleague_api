# Module euroleague_api.team_stats

??? example "View Source"
        from typing import Optional

        import pandas as pd

        from .utils import get_team_stats

        

        def get_team_stats_all_seasons(

            endpoint: str,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            A function that gets the team stats for all seasons

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {"SeasonMode": "All"}

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

        

        def get_team_stats_single_season(

            endpoint: str,

            season: int,

            phase_type_code: str,

            statistic_mode: str

        ) -> pd.DataFrame:

            """

            A function that returns the teams' stats in a single season

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

                season (int): The start year of the season

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

        

        def get_team_stats_range_seasons(

            endpoint: str,

            from_season: int,

            to_season: int,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            A function that returns the teams' stats in a range of seasons

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

                from_season (int): The start year of the start season

                to_season (int): The end year of the end season

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{from_season}",

                "ToSeasonCode": f"E{to_season}",

            }

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

## Functions

    
### get_team_stats_all_seasons

```python3
def get_team_stats_all_seasons(
    endpoint: str,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

A function that gets the team stats for all seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats to fetch. Available values:<br>- traditional<br>- advanced<br>- opponentsTraditional<br>- opponentsAdvanced | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the teams' stats |

??? example "View Source"
        def get_team_stats_all_seasons(

            endpoint: str,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            A function that gets the team stats for all seasons

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {"SeasonMode": "All"}

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

    
### get_team_stats_range_seasons

```python3
def get_team_stats_range_seasons(
    endpoint: str,
    from_season: int,
    to_season: int,
    phase_type_code: Optional[str] = None,
    statistic_mode: str = 'PerGame'
) -> pandas.core.frame.DataFrame
```

A function that returns the teams' stats in a range of seasons

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats to fetch. Available values:<br>- traditional<br>- advanced<br>- opponentsTraditional<br>- opponentsAdvanced | None |
| from_season | int | The start year of the start season | None |
| to_season | int | The end year of the end season | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the teams' stats |

??? example "View Source"
        def get_team_stats_range_seasons(

            endpoint: str,

            from_season: int,

            to_season: int,

            phase_type_code: Optional[str] = None,

            statistic_mode: str = "PerGame"

        ) -> pd.DataFrame:

            """

            A function that returns the teams' stats in a range of seasons

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

                from_season (int): The start year of the start season

                to_season (int): The end year of the end season

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {

                "SeasonMode": "Range",

                "FromSeasonCode": f"E{from_season}",

                "ToSeasonCode": f"E{to_season}",

            }

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df

    
### get_team_stats_single_season

```python3
def get_team_stats_single_season(
    endpoint: str,
    season: int,
    phase_type_code: str,
    statistic_mode: str
) -> pandas.core.frame.DataFrame
```

A function that returns the teams' stats in a single season

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| endpoint | str | The type of stats to fetch. Available values:<br>- traditional<br>- advanced<br>- opponentsTraditional<br>- opponentsAdvanced | None |
| season | int | The start year of the season | None |
| phase_type_code | Optional[str] | The phase of the season,<br>available variables:<br>- "RS" (regular season)<br>- "PO" (play-off)<br>- "FF" (final four)<br>Defaults to None, which includes all phases. | None |
| statistic_mode | str | The aggregation of statistics,<br>available variables:<br>- PerGame<br>- Accumulated<br>Defaults to "PerGame". | None |

**Returns:**

| Type | Description |
|---|---|
| pd.DataFrame | A dataframe with the teams' stats |

??? example "View Source"
        def get_team_stats_single_season(

            endpoint: str,

            season: int,

            phase_type_code: str,

            statistic_mode: str

        ) -> pd.DataFrame:

            """

            A function that returns the teams' stats in a single season

            Args:

                endpoint (str): The type of stats to fetch. Available values:

                    - traditional

                    - advanced

                    - opponentsTraditional

                    - opponentsAdvanced

                season (int): The start year of the season

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

                    Defaults to "PerGame".

            Returns:

                pd.DataFrame: A dataframe with the teams' stats

            """

            params = {

                "SeasonMode": "Single",

                "SeasonCode": f"E{season}",

            }

            df = get_team_stats(endpoint, params, phase_type_code, statistic_mode)

            return df