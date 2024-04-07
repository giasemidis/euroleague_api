# Euroleague API

This is a python package of the Euroleague API for the *Euroleague* and *EuroCup* leagues. The API endpoints were found on the [swagger platform](https://api-live.euroleague.net/swagger/index.html), with the addition of a few more API endpoints (e.g. shot data) found on blogs and discussions. More endpoints will be added.

## Installation

```bash
pip install euroleague-api
```

## Example

```python
euroleague_api.shot_data import ShotData

season = 2022
game_code = 1
competition_code = "E"

shotdata = ShotData(competition_code)
df = shotdata.get_game_shot_data(season, game_code)
```

See also the `notebooks/get-season-stas.ipynb` notebook for examples.

## Documentation

### Euroleague Data class

[EuroleagueData.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/EuroleagueData.html)

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

### Play-by-play data

[play_by_play_data.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/play_by_play_data.html)

### Boxscore data

[boxscore_data.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/boxscore_data.html)

### Auxiliary functions

[utils.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/utils.html)

## TODO

- Add tests
