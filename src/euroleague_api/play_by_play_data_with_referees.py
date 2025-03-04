import requests
import numpy as np
import pandas as pd
from euroleague_api.play_by_play_data import PlayByPlay

# Function to fetch play by play data for a given year and game code along with referees
def get_game_play_by_play_data_with_referees(gamecode, competition_code, season):

    # Getting the play by play data for the match
    pbp_data = PlayByPlay(competition=competition_code)
    pbp = pbp_data.get_game_play_by_play_data(season=season, gamecode=gamecode)
    
    # Define the base URL to pull referee data
    BASE_URL = 'https://live.euroleague.net/api/Header?gamecode={}&seasoncode={}{}&disp='

    # Define the base URL
    url = BASE_URL.format(gamecode, competition_code, season)
    response = requests.get(url)
    
    json_content = response.json()
    referees = [json_content['Referee1'], json_content['Referee2'], json_content['Referee3']]
    pbp['Referees'] = [referees] * len(pbp)

    return pbp