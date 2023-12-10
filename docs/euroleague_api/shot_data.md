# Module euroleague_api.shot_data

??? example "View Source"
        import pandas as pd

        from json.decoder import JSONDecodeError

        from .utils import get_requests

        from .utils import get_season_data_from_game_data

        from .utils import get_range_seasons_data

        MADE_ACTIONS = ['2FGM', '3FGM', 'LAYUPMD', 'DUNK']

        MISSES_ACTIONS = ['2FGA', '2FGAB', '3FGA', '3FGAB', 'LAYUPATT']

        

        def get_game_shot_data(season: int, gamecode: int) -> pd.DataFrame:

            """

            A function that gets the shot data of a particular game.

            Args:

                season (int): The start year of the season

                gamecode (int): The game-code of the game of interest.

                    It can be found on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the shot data of the game.

            """

            url = "https://live.euroleague.net/api/Points"

            params = {

                "gamecode": gamecode,

                "seasoncode": f"E{season}"

            }

            r = get_requests(url, params=params)

            try:

                data = r.json()

            except JSONDecodeError:

                raise ValueError(f"Game code, {gamecode}, did not return any data.")

            shots_df = pd.DataFrame(data['Rows'])

            # team id, player id and action id contain trailing white space

            if not shots_df.empty:

                shots_df['TEAM'] = shots_df['TEAM'].str.strip()

                shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()

                shots_df['ID_ACTION'] = shots_df['ID_ACTION'].str.strip()

                shots_df.insert(0, 'Season', season)

                shots_df.insert(1, 'Gamecode', gamecode)

            return shots_df

        

        def get_game_shot_data_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the shot data of *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the shot data of all games in a single

                    season

            """

            data_df = get_season_data_from_game_data(season, get_game_shot_data)

            return data_df

        

        def get_game_shot_data_multiple_seasons(

            start_season: int, end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the shot data of *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the shot data of all games in range of

                    seasons

            """

            df = get_range_seasons_data(

                start_season, end_season, get_game_shot_data)

            return df

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

??? example "View Source"
        def get_game_shot_data(season: int, gamecode: int) -> pd.DataFrame:

            """

            A function that gets the shot data of a particular game.

            Args:

                season (int): The start year of the season

                gamecode (int): The game-code of the game of interest.

                    It can be found on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the shot data of the game.

            """

            url = "https://live.euroleague.net/api/Points"

            params = {

                "gamecode": gamecode,

                "seasoncode": f"E{season}"

            }

            r = get_requests(url, params=params)

            try:

                data = r.json()

            except JSONDecodeError:

                raise ValueError(f"Game code, {gamecode}, did not return any data.")

            shots_df = pd.DataFrame(data['Rows'])

            # team id, player id and action id contain trailing white space

            if not shots_df.empty:

                shots_df['TEAM'] = shots_df['TEAM'].str.strip()

                shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()

                shots_df['ID_ACTION'] = shots_df['ID_ACTION'].str.strip()

                shots_df.insert(0, 'Season', season)

                shots_df.insert(1, 'Gamecode', gamecode)

            return shots_df

    
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

??? example "View Source"
        def get_game_shot_data_multiple_seasons(

            start_season: int, end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the shot data of *all* games in a range of seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the shot data of all games in range of

                    seasons

            """

            df = get_range_seasons_data(

                start_season, end_season, get_game_shot_data)

            return df

    
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

??? example "View Source"
        def get_game_shot_data_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the shot data of *all* games in a single season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the shot data of all games in a single

                    season

            """

            data_df = get_season_data_from_game_data(season, get_game_shot_data)

            return data_df