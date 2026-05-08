"""
Shared fixtures and utilities for the euroleague_api test suite
"""

import pytest
import pandas as pd
import responses
from unittest.mock import Mock, patch
from src.euroleague_api.EuroLeagueData import EuroLeagueData


@pytest.fixture
def mock_euroleague_data():
    """Create a mock EuroLeagueData instance for testing"""
    return EuroLeagueData(competition="E")


@pytest.fixture
def mock_eurocup_data():
    """Create a mock EuroLeagueData instance for EuroCup"""
    return EuroLeagueData(competition="U")


@pytest.fixture
def sample_game_codes_df():
    """Sample game codes DataFrame for testing"""
    return pd.DataFrame({
        'gameCode': [1, 2, 3],
        'Phase': ['Regular Season', 'Regular Season', 'Playoffs'],
        'Round': [1, 2, 3],
        'played': [True, True, False],
        'homescore': [85, 92, 0],
        'awayscore': [78, 88, 0],
        'home': ['Real Madrid', 'Barcelona', 'Milano'],
        'away': ['CSKA Moscow', 'Fenerbahce', 'Panathinaikos']
    })


@pytest.fixture
def mock_api_response():
    """Mock API response data"""
    return {
        "data": [
            {
                "gameCode": 1,
                "season": 2023,
                "round": 1,
                "played": True,
                "homeTeam": "Real Madrid",
                "awayTeam": "CSKA Moscow"
            }
        ]
    }


@pytest.fixture
def mock_shot_data_response():
    """Mock shot data API response"""
    return {
        "Rows": [
            {
                "PLAYER_ID": "12345",
                "PLAYER": "Player Name",
                "TEAM": "Real Madrid",
                "ACTION": "2FGM",
                "MINUTE": 15,
                "CONSOLE": "15:30",
                "POINTS_A": 10,
                "POINTS_B": 8,
                "COORD_X": 250,
                "COORD_Y": 150,
                "ZONE": "2"
            }
        ]
    }


@pytest.fixture
def mock_boxscore_response():
    """Mock boxscore API response"""
    return {
        "EndOfQuarter": [
            {
                "Team": "Real Madrid",
                "Q1": 20,
                "Q2": 18,
                "Q3": 22,
                "Q4": 25,
                "Total": 85
            }
        ],
        "PlayersStats": [
            {
                "Player": "Player Name",
                "Team": "Real Madrid",
                "MIN": "25:30",
                "PTS": 15,
                "FGM": 6,
                "FGA": 10,
                "Plusminus": 7
            }
        ]
    }


@pytest.fixture
def responses_mock():
    """Setup responses mock for HTTP requests"""
    with responses.RequestsMock() as rsps:
        yield rsps


class MockResponse:
    """Mock response object for testing"""
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.content = str(json_data).encode('utf-8')
    
    def json(self):
        return self.json_data
    
    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception(f"HTTP {self.status_code}")


@pytest.fixture
def mock_requests_get():
    """Mock requests.get function"""
    with patch('requests.get') as mock_get:
        yield mock_get


def assert_dataframe_structure(df, expected_columns, min_rows=0):
    """Helper function to assert DataFrame structure"""
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= min_rows
    for col in expected_columns:
        assert col in df.columns, f"Column '{col}' not found in DataFrame"


def create_mock_xml_response(games_data):
    """Create mock XML response for game codes"""
    games_xml = ""
    for game in games_data:
        games_xml += f"""
        <game>
            <gamenumber>{game['gameCode']}</gamenumber>
            <round>{game['Phase']}</round>
            <gameday>{game['Round']}</gameday>
            <played>{str(game['played']).lower()}</played>
            <homescore>{game['homescore']}</homescore>
            <awayscore>{game['awayscore']}</awayscore>
            <home>{game['home']}</home>
            <away>{game['away']}</away>
        </game>
        """
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <results>
        {games_xml}
    </results>"""
