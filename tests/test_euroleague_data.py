"""
Unit tests for the EuroLeagueData base class.
"""

import pytest
import pandas as pd
import responses
from unittest.mock import patch, Mock
from json.decoder import JSONDecodeError
from src.euroleague_api.EuroLeagueData import EuroLeagueData
from tests.conftest import MockResponse, create_mock_xml_response


class TestEuroLeagueDataInit:
    """Test EuroLeagueData initialization"""
    def test_init_euroleague_competition(self):
        """Test initialization for EuroLeague competition"""
        data = EuroLeagueData(competition="E")
        assert data.competition == "E"
        assert "E" in data.url
        assert "E" in data.url_v2
    
    def test_init_eurocup_competition(self):
        """Test initialization for EuroCup competition"""
        data = EuroLeagueData(competition="U")
        assert data.competition == "U"
        assert "U" in data.url
        assert "U" in data.url_v2
    
    def test_init_default_competition(self):
        """Test initialization with default competition"""
        data = EuroLeagueData()
        assert data.competition == "E"
    
    def test_init_invalid_competition(self):
        """Test initialization with invalid competition raises ValueError"""
        with pytest.raises(ValueError, match="Invalid competition value"):
            EuroLeagueData(competition="X")
    
    def test_url_construction(self):
        """Test URL construction for different API versions"""
        data = EuroLeagueData(competition="E")
        
        expected_base = "https://api-live.euroleague.net"
        assert data.BASE_URL == expected_base
        assert data.url_v1 == f"{expected_base}/v1/results/"
        assert data.url_v2 == f"{expected_base}/v2/competitions/E"
        assert data.url == f"{expected_base}/v3/competitions/E"


class TestEuroLeagueDataMethods:
    """Test EuroLeagueData methods"""
    def test_make_season_game_url(self):
        """Test season game URL construction for EuroLeague"""
        data = EuroLeagueData(competition="E")
        url = data.make_season_game_url(2024, 5, "boxscore")
        
        expected = (
            "https://api-live.euroleague.net/v3/competitions/E/"
            "seasons/E2024/games/5/boxscore"
        )
        assert url == expected
    
    def test_make_season_game_url_eurocup(self):
        """Test season game URL construction for EuroCup"""
        data = EuroLeagueData(competition="U")
        url = data.make_season_game_url(2024, 5, "stats")
        
        expected = (
            "https://api-live.euroleague.net/v3/competitions/U/"
            "seasons/U2024/games/5/stats"
        )
        assert url == expected


class TestGetGamecodesSeason:
    """Test get_gamecodes_season method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_gamecodes_season_success(self, mock_get_requests):
        """Test successful retrieval of season game codes"""
        # Mock XML response
        mock_games = [
            {
                'gameCode': 1, 'Phase': 'Regular Season', 'Round': 1,
                'played': True, 'homescore': 85, 'awayscore': 78,
                'home': 'Real Madrid', 'away': 'CSKA Moscow'
            },
            {
                'gameCode': 2, 'Phase': 'Regular Season', 'Round': 2,
                'played': True, 'homescore': 92, 'awayscore': 88,
                'home': 'Barcelona', 'away': 'Fenerbahce'
            }
        ]
        
        xml_content = create_mock_xml_response(mock_games)
        mock_response = Mock()
        mock_response.content = xml_content.encode('utf-8')
        mock_get_requests.return_value = mock_response
        
        data = EuroLeagueData(competition="E")
        df = data.get_gamecodes_season(2024)

        # Verify the request
        mock_get_requests.assert_called_once()
        args, kwargs = mock_get_requests.call_args
        assert args[0] == data.url_v1
        assert kwargs['params']['seasonCode'] == 'E2024'
        
        # Verify DataFrame structure and content
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'gameCode' in df.columns
        assert 'Phase' in df.columns
        assert 'Round' in df.columns
        assert 'played' in df.columns
        
        # Check data types
        assert df['gameCode'].dtype == 'int64'
        assert df['Round'].dtype == 'int64'
        assert df['played'].dtype == 'bool'
        
        # Check sorting
        assert df['gameCode'].iloc[0] == 1
        assert df['gameCode'].iloc[1] == 2


class TestGetGamecodesRound:
    """Test get_gamecodes_round method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_gamecodes_round_success(self, mock_get_requests):
        """Test successful retrieval of round game codes"""
        mock_response_data = {
            "data": [
                {
                    "gameCode": 1,
                    "round": 1,
                    "phaseType": {"code": "RS"},
                    "played": True,
                    "homeTeam": {"name": "Real Madrid"},
                    "awayTeam": {"name": "CSKA Moscow"}
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        data = EuroLeagueData(competition="E")
        df = data.get_gamecodes_round(2024, 5)
        
        # Verify the request
        mock_get_requests.assert_called_once()
        args, kwargs = mock_get_requests.call_args
        expected_url = f"{data.url_v2}/seasons/E2024/games"
        assert args[0] == expected_url
        assert kwargs['params']['roundNumber'] == 5

        # Verify DataFrame
        assert isinstance(df, pd.DataFrame)
        assert len(df) >= 1
        assert 'gameCode' in df.columns
        assert 'Round' in df.columns
        assert 'Phase' in df.columns
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_gamecodes_round_invalid_round(self, mock_get_requests):
        """Test handling of invalid round number."""
        # Mock response that returns invalid JSON
        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError("Invalid JSON", "", 0)
        mock_get_requests.return_value = mock_response
        
        data = EuroLeagueData(competition="E")
        
        with pytest.raises(ValueError, match="Round, 99, season 2024"):
            data.get_gamecodes_round(2024, 99)


class TestDataCollectionMethods:
    """Test data collection wrapper methods"""
    def test_get_round_data_from_game_data(self):
        """Test round data collection wrapper"""
        data = EuroLeagueData(competition="E")

        # Mock the get_gamecodes_round method
        mock_games_df = pd.DataFrame({
            'gameCode': [1, 2],
            'Phase': ['Regular Season', 'Regular Season'],
            'Round': [1, 1],
            'played': [True, True]
        })
        
        # Mock function to collect data
        def mock_fun(season, game_code):
            return pd.DataFrame({
                'gameCode': [game_code],
                'season': [season],
                'stat': [10]
            })
        
        with patch.object(data, 'get_gamecodes_round', return_value=mock_games_df):
            with patch('src.euroleague_api.utils.get_data_over_collection_of_games') as mock_get_data:
                mock_get_data.return_value = pd.DataFrame({'result': [1, 2]})

                result = data.get_round_data_from_game_data(2024, 5, mock_fun)

                mock_get_data.assert_called_once()
                assert isinstance(result, pd.DataFrame)
    
    def test_get_season_data_from_game_data(self):
        """Test season data collection wrapper"""
        data = EuroLeagueData(competition="E")
        
        mock_games_df = pd.DataFrame({
            'gameCode': [1, 2, 3],
            'Phase': ['Regular Season', 'Regular Season', 'Playoffs'],
            'Round': [1, 2, 3],
            'played': [True, True, True]
        })
        
        def mock_fun(season, game_code):
            return pd.DataFrame({'gameCode': [game_code], 'data': [1]})
        
        with patch.object(data, 'get_gamecodes_season', return_value=mock_games_df):
            with patch('src.euroleague_api.utils.get_data_over_collection_of_games') as mock_get_data:
                mock_get_data.return_value = pd.DataFrame({'result': [1, 2, 3]})
                result = data.get_season_data_from_game_data(2024, mock_fun)

                mock_get_data.assert_called_once()
                assert isinstance(result, pd.DataFrame)
    
    def test_get_range_seasons_data(self):
        """Test multi-season data collection"""
        data = EuroLeagueData(competition="E")
        
        def mock_fun(season, game_code):
            return pd.DataFrame({'season': [season], 'data': [1]})
        
        with patch.object(data, 'get_season_data_from_game_data') as mock_season_data:
            mock_season_data.side_effect = [
                pd.DataFrame({'season': [2023], 'data': [1]}),
                pd.DataFrame({'season': [2024], 'data': [2]})
            ]
            result = data.get_range_seasons_data(2022, 2024, mock_fun)

            assert mock_season_data.call_count == 2
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            assert 2023 in result['season'].values
            assert 2024 in result['season'].values


@pytest.mark.integration
class TestEuroLeagueDataIntegration:
    """Integration tests that make real API calls"""
    @pytest.mark.slow
    def test_real_api_call_gamecodes_season(self):
        """Test real API call for game codes"""
        data = EuroLeagueData(competition="E")
        
        # Use a known season that should have data
        try:
            df = data.get_gamecodes_season(2024)
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0
            assert 'gameCode' in df.columns
        except Exception as e:
            pytest.skip(f"API call failed: {e}")
