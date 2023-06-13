# Euroleague API

This is a python package of the Euroleague API. The API endpoints were found on the [swagger platform](https://api-live.euroleague.net/swagger/index.html), with the addition of a few more API endpoints (e.g. shot data) found on blogs and discussions. More endpoints will be added.

TODO:
- publish on pypi
- tests

## Example
```python
from euroleague_api import shot_data

season = 2022
game_code = 1

df = shot_data.get_game_shot_data(season, game_code)
```

## Documentation

### Game stats
[game_stats.py](docs/euroleague_api/game_stats.md)

### Player stats
[player_stats.py](docs/euroleague_api/player_stats.md)

### Team stats
[team_stats.py](docs/euroleague_api/team_stats.md)

### Standings
[standings.py](docs/euroleague_api/standings.md)

### Shot data
[shot_data.py](docs/euroleague_api/shot_data.md)

### Auxiliary functions
[utils.py](docs/euroleague_api/utils.md)
