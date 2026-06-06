
<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=giasemidis&project=euroleague_api&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

# Euroleague API

This is a python package of the Euroleague API for the *Euroleague* and *EuroCup* leagues. The API endpoints were found on the [swagger platform](https://api-live.euroleague.net/swagger/index.html), with the addition of a few more API endpoints (e.g. shot data) found on blogs and discussions. More endpoints will be added.

If you like this library, consider donating on


<a href="https://www.buymeacoffee.com/georgios.giasemidis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Installation

```bash
pip install euroleague-api
```

## Example

```python
from euroleague_api.shot_data import ShotData

season = 2022
game_code = 1
competition_code = "E"

shotdata = ShotData(competition_code)
df = shotdata.get_game_shot_data(season, game_code)
```

See also the `notebooks/get-season-stats.ipynb` notebook for examples.

## Documentation

### Euroleague Data class

[EuroleagueData.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/EuroLeagueData.html)

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

### Game Metadata

[game_metadata.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/game_metadata.html)

### League Schedule
[schedule.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/schedule.html)

### Auxiliary functions

[utils.py](https://htmlpreview.github.io/?https://github.com/giasemidis/euroleague_api/blob/main/site/euroleague_api/utils.html)

## TODO

- Add tests
