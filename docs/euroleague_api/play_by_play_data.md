# Module euroleague_api.play_by_play_data

??? example "View Source"
        from json.decoder import JSONDecodeError

        import pandas as pd

        from .utils import get_requests

        from .utils import get_season_data_from_game_data

        from .utils import get_range_seasons_data

        

        def get_game_play_by_play_data(season: int, gamecode: int) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of a particular game.

            Args:

                season (int): The start year of the season

                gamecode (int): The game-code of the game of interest.

                    It can be found on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of the game.

            """

            url = "https://live.euroleague.net/api/PlaybyPlay"

            params = {

                "gamecode": gamecode,

                "seasoncode": f"E{season}"

            }

            r = get_requests(url, params=params)

            try:

                data = r.json()

            except JSONDecodeError:

                raise ValueError(f"Game code, {gamecode}, did not return any data.")

            periods = [

                'FirstQuarter', 'SecondQuarter', 'ThirdQuarter', 'ForthQuarter',

                'ExtraTime'

            ]

            all_data = []

            for p, period in enumerate(periods):

                if data[period]:

                    df = pd.json_normalize(data[period])

                    df["PERIOD"] = p + 1

                    all_data.append(df)

            play_by_play_df = pd.concat(all_data)

            play_by_play_df['CODETEAM'] = play_by_play_df['CODETEAM'].str.strip()

            play_by_play_df['PLAYER_ID'] = play_by_play_df['PLAYER_ID'].str.strip()

            play_by_play_df.insert(0, 'Season', season)

            play_by_play_df.insert(1, 'Gamecode', gamecode)

            return play_by_play_df

        

        def get_game_play_by_play_data_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of *all* games in a single

            season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of all games in a

                    single season

            """

            data_df = get_season_data_from_game_data(

                season, get_game_play_by_play_data)

            return data_df

        

        def get_game_play_by_play_data_multiple_seasons(

            start_season: int, end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of *all* games in a range of

            seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of all games

                    in range of seasons

            """

            df = get_range_seasons_data(

                start_season, end_season, get_game_play_by_play_data)

            return df

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

??? example "View Source"
        def get_game_play_by_play_data(season: int, gamecode: int) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of a particular game.

            Args:

                season (int): The start year of the season

                gamecode (int): The game-code of the game of interest.

                    It can be found on Euroleague's website.

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of the game.

            """

            url = "https://live.euroleague.net/api/PlaybyPlay"

            params = {

                "gamecode": gamecode,

                "seasoncode": f"E{season}"

            }

            r = get_requests(url, params=params)

            try:

                data = r.json()

            except JSONDecodeError:

                raise ValueError(f"Game code, {gamecode}, did not return any data.")

            periods = [

                'FirstQuarter', 'SecondQuarter', 'ThirdQuarter', 'ForthQuarter',

                'ExtraTime'

            ]

            all_data = []

            for p, period in enumerate(periods):

                if data[period]:

                    df = pd.json_normalize(data[period])

                    df["PERIOD"] = p + 1

                    all_data.append(df)

            play_by_play_df = pd.concat(all_data)

            play_by_play_df['CODETEAM'] = play_by_play_df['CODETEAM'].str.strip()

            play_by_play_df['PLAYER_ID'] = play_by_play_df['PLAYER_ID'].str.strip()

            play_by_play_df.insert(0, 'Season', season)

            play_by_play_df.insert(1, 'Gamecode', gamecode)

            return play_by_play_df

    
### get_game_play_by_play_data_multiple_seasons

```python3
def get_game_play_by_play_data_multiple_seasons(
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

??? example "View Source"
        def get_game_play_by_play_data_multiple_seasons(

            start_season: int, end_season: int

        ) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of *all* games in a range of

            seasons

            Args:

                start_season (int): The start year of the start season

                end_season (int): The start year of the end season

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of all games

                    in range of seasons

            """

            df = get_range_seasons_data(

                start_season, end_season, get_game_play_by_play_data)

            return df

    
### get_game_play_by_play_data_single_season

```python3
def get_game_play_by_play_data_single_season(
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

??? example "View Source"
        def get_game_play_by_play_data_single_season(season: int) -> pd.DataFrame:

            """

            A function that gets the play-by-play data of *all* games in a single

            season

            Args:

                season (int): The start year of the season

            Returns:

                pd.DataFrame: A dataframe with the play-by-play data of all games in a

                    single season

            """

            data_df = get_season_data_from_game_data(

                season, get_game_play_by_play_data)

            return data_df