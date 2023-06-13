# Module euroleague_api.standings

## Variables

```python3
URL
```

## Functions

    
### get_standings

```python3
def get_standings(
    season: int,
    round_number: int,
    endpoint: str = 'basicstandings'
) -> pandas.core.frame.DataFrame
```

Get the standings of round in given season

Args:

    season (int): The start year of the season

    round_number (int): The round number

    endpoint (str, optional): The type of standing.
    One of the following options
    - calendarstandings
    - streaks
    - aheadbehind
    - margins
    - basicstandings
    Defaults to "basicstandings".

Raises:

    ValueError: If endpoint is not applicable

Returns:

    pd.DataFrame: A dataframe with the standings of the teams
