# Euroleague API

This is a python package of the Euroleague API. The API endpoints were found on the [swagger platform](https://api-live.euroleague.net/swagger/index.html), with the addition of a few more API endpoints (e.g. shot data) found on blogs and discussions. More endpoints will be added.

## Installation

```
pip install euroleague-api
```

## Example
```python
from euroleague_api import shot_data

season = 2022
game_code = 1

df = shot_data.get_game_shot_data(season, game_code)
```

## Documentation

### Game stats
[game_stats.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/game_stats.html)

### Player stats
[player_stats.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/player_stats.html)

### Team stats
[team_stats.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/team_stats.html)

### Standings
[standings.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/standings.html)

### Shot data
[shot_data.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/shot_data.html)

### Auxiliary functions
[utils.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_ap/utils.html)

## TODO
- Add more endpoints from various sources
- Add Eurocup API support
- Add tests
