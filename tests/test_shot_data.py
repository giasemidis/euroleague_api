"""
Unit tests for the ShotData class.
"""

import pytest
import pandas as pd
import responses
from unittest.mock import patch, Mock
from json.decoder import JSONDecodeError
from src.euroleague_api.shot_data import ShotData
from tests.conftest import MockResponse


class TestShotDataInit:
    """Test ShotData initialization"""
    def test_init_euroleague(self):
        """Test initialization for EuroLeague competition"""
        shot_data = ShotData(competition="E")
        assert shot_data.competition == "E"
        assert isinstance(shot_data, ShotData)
    
    def test_init_eurocup(self):
        """Test initialization for EuroCup competition"""
        shot_data = ShotData(competition="U")
        assert shot_data.competition == "U"
    
    def test_init_default(self):
        """Test initialization with default competition"""
        shot_data = ShotData()
        assert shot_data.competition == "E"
    
    def test_init_invalid_competition(self):
        """Test initialization with invalid competition"""
        with pytest.raises(ValueError, match="Invalid competition value"):
            ShotData(competition="X")


class TestGetGameShotData:
    """Test get_game_shot_data method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_shot_data_success(self, mock_get_requests):
        """Test successful shot data retrieval"""
        mock_response_data = {
            "Rows": [
                {
                    "PLAYER_ID": "12345",
                    "PLAYER": "John Doe",
                    "TEAM": "Real Madrid",
                    "ACTION": "2FGM",
                    "MINUTE": 15,
                    "CONSOLE": "15:30",
                    "POINTS_A": 10,
                    "POINTS_B": 8,
                    "COORD_X": 250,
                    "COORD_Y": 150,
                    "ZONE": "2",
                    "FASTBREAK": 0,
                    "SECOND_CHANCE": 0,
                    "POINTS_OFF_TURNOVER": 0
                },
                {
                    "PLAYER_ID": "67890",
                    "PLAYER": "Jane Doe",
                    "TEAM": "Barcelona",
                    "ACTION": "3FGM",
                    "MINUTE": 25,
                    "CONSOLE": "25:45",
                    "POINTS_A": 15,
                    "POINTS_B": 12,
                    "COORD_X": 300,
                    "COORD_Y": 200,
                    "ZONE": "3",
                    "FASTBREAK": 1,
                    "SECOND_CHANCE": 0,
                    "POINTS_OFF_TURNOVER": 1
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        shot_data = ShotData(competition="E")
        result = shot_data.get_game_shot_data(2024, 5)
        
        # Verify the request
        mock_get_requests.assert_called_once()
        args, kwargs = mock_get_requests.call_args
        assert args[0] == "https://live.euroleague.net/api/Points"
        assert kwargs['params']['gamecode'] == 5
        assert kwargs['params']['seasoncode'] == "E2024"

        # Verify DataFrame structure and content
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        
        expected_columns = [
            'PLAYER_ID', 'PLAYER', 'TEAM', 'ACTION', 'MINUTE', 'CONSOLE',
            'POINTS_A', 'POINTS_B', 'COORD_X', 'COORD_Y', 'ZONE',
            'FASTBREAK', 'SECOND_CHANCE', 'POINTS_OFF_TURNOVER'
        ]
        
        for col in expected_columns:
            assert col in result.columns
        
        # Check specific values
        assert result['PLAYER'].iloc[0] == "John Doe"
        assert result['ACTION'].iloc[0] == "2FGM"
        assert result['TEAM'].iloc[0] == "Real Madrid"
        assert result['COORD_X'].iloc[0] == 250
        
        assert result['PLAYER'].iloc[1] == "Jane Doe"
        assert result['ACTION'].iloc[1] == "3FGM"
        assert result['FASTBREAK'].iloc[1] == 1
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_shot_data_eurocup(self, mock_get_requests):
        """Test shot data retrieval for EuroCup"""
        mock_response_data = {"Rows": []}
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        shot_data = ShotData(competition="U")
        result = shot_data.get_game_shot_data(2024, 5)
        
        # Verify correct competition code in request
        args, kwargs = mock_get_requests.call_args
        assert kwargs['params']['seasoncode'] == "U2024"
        assert kwargs['params']['gamecode'] == 5
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_shot_data_json_decode_error(self, mock_get_requests):
        """Test handling of JSON decode error"""
        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError("Invalid JSON", "", 0)
        mock_get_requests.return_value = mock_response
        
        shot_data = ShotData(competition="E")

        with pytest.raises(ValueError, match="Game code, 999, season 2024"):
            shot_data.get_game_shot_data(2024, 999)

    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_shot_data_empty_response(self, mock_get_requests):
        """Test handling of empty shot data response"""
        mock_response_data = {"Rows": []}
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        shot_data = ShotData(competition="E")
        result = shot_data.get_game_shot_data(2024, 1)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0


class TestGetGameShotDataSingleSeason:
    """Test get_game_shot_data_single_season method"""
    
    def test_get_game_shot_data_single_season(self):
        """Test single season shot data collection"""
        shot_data = ShotData(competition="E")
        
        # Mock the parent class method
        mock_season_data = pd.DataFrame({
            'gameCode': [1, 2],
            'PLAYER': ['Player1', 'Player2'],
            'ACTION': ['2FGM', '3FGM'],
            'POINTS_A': [10, 15],
            'POINTS_B': [8, 12]
        })
        
        with patch.object(shot_data, 'get_season_data_from_game_data', 
                         return_value=mock_season_data) as mock_method:
            result = shot_data.get_game_shot_data_single_season(2024)
            
            # Verify the method was called with correct parameters
            mock_method.assert_called_once_with(2024, shot_data.get_game_shot_data)
            
            # Verify the result
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            pd.testing.assert_frame_equal(result, mock_season_data)


class TestGetGameShotDataMultipleSeasons:
    """Test get_game_shot_data_multiple_seasons method"""
    
    def test_get_game_shot_data_multiple_seasons(self):
        """Test multiple seasons shot data collection"""
        shot_data = ShotData(competition="E")
        
        # Mock the parent class method
        mock_range_data = pd.DataFrame({
            'season': [2023, 2023, 2024, 2024],
            'gameCode': [1, 2, 1, 2],
            'PLAYER': ['Player1', 'Player2', 'Player3', 'Player4'],
            'ACTION': ['2FGM', '3FGM', '2FGM', '3FGM'],
            'POINTS_A': [10, 15, 12, 18],
            'POINTS_B': [8, 12, 10, 16]
        })
        
        with patch.object(shot_data, 'get_range_seasons_data', 
                         return_value=mock_range_data) as mock_method:
            result = shot_data.get_game_shot_data_multiple_seasons(2023, 2024)
            
            # Verify the method was called with correct parameters
            mock_method.assert_called_once_with(2023, 2024, shot_data.get_game_shot_data)

            # Verify the result
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 4
            pd.testing.assert_frame_equal(result, mock_range_data)
    
    def test_get_game_shot_data_multiple_seasons_single_season(self):
        """Test multiple seasons method with single season (start == end)"""
        shot_data = ShotData(competition="E")
        
        mock_range_data = pd.DataFrame({
            'season': [2024],
            'gameCode': [1],
            'PLAYER': ['Player1'],
            'ACTION': ['2FGM']
        })
        
        with patch.object(shot_data, 'get_range_seasons_data', 
                         return_value=mock_range_data) as mock_method:
            result = shot_data.get_game_shot_data_multiple_seasons(2024, 2024)

            mock_method.assert_called_once_with(2024, 2024, shot_data.get_game_shot_data)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1


@pytest.mark.integration
class TestShotDataIntegration:
    """Integration tests for ShotData class"""
    @pytest.mark.slow
    def test_real_shot_data_api_call(self):
        """Test real API call for shot data"""
        shot_data = ShotData(competition="E")

        # Use a known game that should have shot data
        try:
            result = shot_data.get_game_shot_data(2024, 1)
            assert isinstance(result, pd.DataFrame)
            # Checking that it's a valid DataFrame
        except ValueError as e:
            # If the specific game doesn't exist, test will continue
            if "did not return any data" in str(e):
                pytest.skip("Test game does not exist or has no shot data")
            else:
                raise
        except Exception as e:
            pytest.skip(f"API call failed: {e}")


class TestShotDataErrorHandling:
    """Test error handling in ShotData class"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_network_error_handling(self, mock_get_requests):
        """Test handling of network errors"""
        mock_get_requests.side_effect = ConnectionError("Network error")
        
        shot_data = ShotData(competition="E")
        
        with pytest.raises(ConnectionError):
            shot_data.get_game_shot_data(2024, 1)
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_malformed_response_handling(self, mock_get_requests):
        """Test handling of malformed API responses"""
        # Response missing 'Rows' key
        mock_response_data = {"InvalidKey": "data"}
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        shot_data = ShotData(competition="E")
        
        with pytest.raises(KeyError):
            shot_data.get_game_shot_data(2024, 1)
