"""
Unit tests for the BoxScoreData class
"""

import pytest
import pandas as pd
from unittest.mock import patch, Mock
from json.decoder import JSONDecodeError
from src.euroleague_api.boxscore_data import BoxScoreData
from tests.conftest import MockResponse


class TestBoxScoreDataInit:
    """Test BoxScoreData initialization"""
    
    def test_init_euroleague(self):
        """Test initialization with EuroLeague competition"""
        boxscore = BoxScoreData(competition="E")
        assert boxscore.competition == "E"
        assert isinstance(boxscore, BoxScoreData)
    
    def test_init_eurocup(self):
        """Test initialization with EuroCup competition"""
        boxscore = BoxScoreData(competition="U")
        assert boxscore.competition == "U"
    
    def test_init_default(self):
        """Test initialization with default competition"""
        boxscore = BoxScoreData()
        assert boxscore.competition == "E"


class TestGetBoxscoreData:
    """Test get_boxscore_data method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_boxscore_data_success(self, mock_get_requests):
        """Test successful boxscore data retrieval"""
        mock_response_data = {
            "EndOfQuarter": [
                {
                    "Team": "Real Madrid",
                    "Q1": "20",
                    "Q2": "18", 
                    "Q3": "22",
                    "Q4": "25",
                    "Total": "85"
                },
                {
                    "Team": "Barcelona",
                    "Q1": "18",
                    "Q2": "20",
                    "Q3": "24",
                    "Q4": "23", 
                    "Total": "85"
                }
            ],
            "PlayersStats": [
                {
                    "Player": "John Doe",
                    "Team": "Real Madrid",
                    "MIN": "25:30",
                    "PTS": "15",
                    "FGM": "6",
                    "FGA": "10",
                    "Plusminus": "7"
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        result = boxscore.get_boxscore_data(2023, 1, "EndOfQuarter")
        
        # Verify the request
        mock_get_requests.assert_called_once()
        args, kwargs = mock_get_requests.call_args
        expected_url = boxscore.make_season_game_url(2023, 1, "boxscore")
        assert args[0] == expected_url
        
        # Verify the result
        assert result == mock_response_data["EndOfQuarter"]
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_boxscore_data_invalid_type(self, mock_get_requests):
        """Test handling of invalid boxscore type"""
        mock_response_data = {"EndOfQuarter": []}
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        
        with pytest.raises(ValueError, match="InvalidType.*is not applicable"):
            boxscore.get_boxscore_data(2023, 1, "InvalidType")
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_boxscore_data_json_decode_error(self, mock_get_requests):
        """Test handling of decode error"""
        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError("Invalid JSON", "", 0)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        
        with pytest.raises(ValueError, match="Game code, 999, season 2023"):
            boxscore.get_boxscore_data(2023, 999, "EndOfQuarter")


class TestGetGameBoxscoreQuarterData:
    """Test get_game_boxscore_quarter_data method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_boxscore_quarter_data_success(self, mock_get_requests):
        """Test successful quarter boxscore data retrieval"""
        mock_response_data = {
            "EndOfQuarter": [
                {
                    "Team": "Real Madrid",
                    "Q1": "20",
                    "Q2": "18",
                    "Q3": "22", 
                    "Q4": "25",
                    "Total": "85"
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        result = boxscore.get_game_boxscore_quarter_data(2023, 1)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert "Team" in result.columns
        assert "Q1" in result.columns
        assert "Total" in result.columns
        
        # Check data conversion
        assert result["Q1"].iloc[0] == 20
        assert result["Total"].iloc[0] == 85
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_game_boxscore_quarter_data_invalid_type(self, mock_get_requests):
        """Test handling of invalid quarter boxscore type"""
        boxscore = BoxScoreData(competition="E")
        
        with pytest.raises(ValueError, match="InvalidQuarterType.*is not applicable"):
            boxscore.get_game_boxscore_quarter_data(2023, 1, "InvalidQuarterType")


class TestGetPlayerBoxscoreStatsData:
    """Test get_player_boxscore_stats_data method"""
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_player_boxscore_stats_data_success(self, mock_get_requests):
        """Test successful player boxscore stats retrieval"""
        mock_response_data = {
            "PlayersStats": [
                {
                    "Player": "John Doe",
                    "Team": "Real Madrid",
                    "MIN": "25:30",
                    "PTS": "15",
                    "FGM": "6",
                    "FGA": "10",
                    "Plusminus": "7"
                },
                {
                    "Player": "Jane Doe",
                    "Team": "Barcelona",
                    "MIN": "30:00",
                    "PTS": "20",
                    "FGM": "8",
                    "FGA": "12",
                    "Plusminus": None
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        result = boxscore.get_player_boxscore_stats_data(2023, 1)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "Player" in result.columns
        assert "Team" in result.columns
        assert "PTS" in result.columns
        assert "Plusminus" in result.columns
        
        # Check data conversion
        assert result["PTS"].iloc[0] == 15
        assert result["FGM"].iloc[0] == 6
        
        # Check None handling for Plusminus
        assert pd.isna(result["Plusminus"].iloc[1])
        assert result["Plusminus"].iloc[0] == 7
    
    @patch('src.euroleague_api.utils.get_requests')
    def test_get_player_boxscore_stats_data_no_plusminus(self, mock_get_requests):
        """Test player boxscore stats without Plusminus column"""
        mock_response_data = {
            "PlayersStats": [
                {
                    "Player": "John Doe",
                    "Team": "Real Madrid",
                    "PTS": "15"
                }
            ]
        }
        
        mock_response = MockResponse(mock_response_data)
        mock_get_requests.return_value = mock_response
        
        boxscore = BoxScoreData(competition="E")
        result = boxscore.get_player_boxscore_stats_data(2023, 1)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1


class TestBoxScoreDataSeasonMethods:
    """Test season-level data collection methods"""
    def test_get_game_boxscore_quarter_data_single_season(self):
        """Test single season quarter data collection"""
        boxscore = BoxScoreData(competition="E")
        
        mock_season_data = pd.DataFrame({
            'gameCode': [1, 2],
            'Team': ['Real Madrid', 'Barcelona'],
            'Q1': [20, 18],
            'Total': [85, 88]
        })
        
        with patch.object(boxscore, 'get_season_data_from_game_data', 
                         return_value=mock_season_data) as mock_method:
            result = boxscore.get_game_boxscore_quarter_data_single_season(2023)
            
            mock_method.assert_called_once_with(2023, boxscore.get_game_boxscore_quarter_data)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            pd.testing.assert_frame_equal(result, mock_season_data)
    
    def test_get_player_boxscore_stats_single_season(self):
        """Test single season player stats collection"""
        boxscore = BoxScoreData(competition="E")
        
        mock_season_data = pd.DataFrame({
            'gameCode': [1, 2],
            'Player': ['Player1', 'Player2'],
            'Team': ['Real Madrid', 'Barcelona'],
            'PTS': [15, 20]
        })
        
        with patch.object(boxscore, 'get_season_data_from_game_data', 
                         return_value=mock_season_data) as mock_method:
            result = boxscore.get_player_boxscore_stats_single_season(2023)
            
            mock_method.assert_called_once_with(2023, boxscore.get_player_boxscore_stats_data)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            pd.testing.assert_frame_equal(result, mock_season_data)


@pytest.mark.integration
class TestBoxScoreDataIntegration:
    """Integration tests for BoxScoreData class"""
    @pytest.mark.slow
    def test_real_boxscore_api_call(self):
        """Test real API call for boxscore data"""
        boxscore = BoxScoreData(competition="E")
        try:
            result = boxscore.get_game_boxscore_quarter_data(2023, 1)
            assert isinstance(result, pd.DataFrame)
        except ValueError as e:
            if "did not return any data" in str(e):
                pytest.skip("Test game does not exist or has no boxscore data")
            else:
                raise
        except Exception as e:
            pytest.skip(f"API call failed: {e}")
