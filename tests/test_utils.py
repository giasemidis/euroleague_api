"""
Unit tests for the utils module.
"""

import pytest
import pandas as pd
import requests
from unittest.mock import Mock, patch
from requests.exceptions import HTTPError
from src.euroleague_api.utils import get_requests, raise_error, get_data_over_collection_of_games


class TestGetRequests:
    """Test the get_requests utility function"""
    @patch('requests.get')
    def test_get_requests_success(self, mock_get):
        """Test successful GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response
        
        url = "https://api.example.com/data"
        params = {"param1": "value1"}
        headers = {"Accept": "application/json"}
        
        result = get_requests(url, params=params, headers=headers)
        
        mock_get.assert_called_once_with(
            url, params=params, headers=headers, timeout=60
        )
        assert result == mock_response
        assert result.status_code == 200
    
    @patch('requests.get')
    def test_get_requests_with_defaults(self, mock_get):
        """Test GET request with default parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        url = "https://api.example.com/data"
        result = get_requests(url)
        
        mock_get.assert_called_once_with(
            url, 
            params={}, 
            headers={"Accept": "application/json"}, 
            timeout=60
        )
        assert result == mock_response
    
    @patch('requests.get')
    def test_get_requests_http_error(self, mock_get):
        """Test GET request with HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        url = "https://api.example.com/nonexistent"
        
        with pytest.raises(HTTPError):
            get_requests(url)
        
        mock_response.raise_for_status.assert_called_once()
    
    @patch('requests.get')
    def test_get_requests_server_error(self, mock_get):
        """Test GET request with server error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_get.return_value = mock_response
        
        url = "https://api.example.com/error"
        
        with pytest.raises(HTTPError):
            get_requests(url)


class TestRaiseError:
    """Test the raise_error utility function"""
    
    def test_raise_error_valid_value(self):
        """Test that no error is raised for valid values"""
        available_values = ["option1", "option2", "option3"]
        
        # Should not raise any exception
        raise_error("option1", "Test parameter", available_values)
        raise_error("option2", "Test parameter", available_values)
        raise_error("option3", "Test parameter", available_values)
    
    def test_raise_error_invalid_value(self):
        """Test that ValueError is raised for invalid values"""
        available_values = ["option1", "option2", "option3"]
        
        with pytest.raises(ValueError, match="Test parameter, invalid_option, is not applicable"):
            raise_error("invalid_option", "Test parameter", available_values)
    
    def test_raise_error_none_not_allowed(self):
        """Test that ValueError is raised when None is not allowed"""
        available_values = ["option1", "option2"]
        
        with pytest.raises(ValueError, match="Test parameter, None, is not applicable"):
            raise_error(None, "Test parameter", available_values, allow_none=False)
    
    def test_raise_error_none_allowed(self):
        """Test that None is accepted when allow_none=True"""
        available_values = ["option1", "option2"]
        
        # Should not raise any exception
        raise_error(None, "Test parameter", available_values, allow_none=True)
    
    def test_raise_error_message_format(self):
        """Test the error message format"""
        available_values = ["A", "B", "C"]
        
        with pytest.raises(ValueError) as excinfo:
            raise_error("X", "My parameter", available_values)
        
        error_message = str(excinfo.value)
        assert "My parameter, X, is not applicable" in error_message
        assert "Available values: ['A', 'B', 'C', None]" in error_message


class TestGetDataOverCollectionOfGames:
    """Test the get_data_over_collection_of_games utility function"""
    
    def test_successful_data_collection(self):
        """Test successful data collection over multiple games"""
        # Mock game codes DataFrame
        game_codes_df = pd.DataFrame({
            'gameCode': [1, 2, 3],
            'Phase': ['Regular Season', 'Regular Season', 'Playoffs'],
            'Round': [1, 1, 2]
        })
        
        # Mock function that returns data for each game
        def mock_fun(season, game_code):
            return pd.DataFrame({
                'gameCode': [game_code],
                'season': [season],
                'points': [game_code * 10]
            })
        
        season = 2024
        result = get_data_over_collection_of_games(game_codes_df, season, mock_fun)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'gameCode' in result.columns
        assert 'season' in result.columns
        assert 'points' in result.columns
        assert 'Phase' in result.columns
        assert 'Round' in result.columns
        
        # Check that Phase and Round were added correctly
        assert result['Phase'].iloc[0] == 'Regular Season'
        assert result['Round'].iloc[0] == 1
    
    def test_empty_dataframe_handling(self):
        """Test handling of functions that return empty DataFrames"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1, 2],
            'Phase': ['Regular Season', 'Regular Season'],
            'Round': [1, 1]
        })
        
        call_count = 0
        def mock_fun(season, game_code):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return pd.DataFrame()  # Empty DataFrame
            else:
                return pd.DataFrame({
                    'gameCode': [game_code],
                    'season': [season],
                    'data': [1]
                })
        
        with patch('src.euroleague_api.utils.logger') as mock_logger:
            result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
            
            # Should log warning for empty DataFrame
            mock_logger.warning.assert_called()
            warning_call = mock_logger.warning.call_args[0][0]
            assert "returned no data" in warning_call
            
            # Should return data from the second game only
            assert len(result) == 1
            assert result['gameCode'].iloc[0] == 2
    
    def test_http_error_handling(self):
        """Test handling of HTTP errors during data collection"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1, 2],
            'Phase': ['Regular Season', 'Regular Season'],
            'Round': [1, 1]
        })
        
        call_count = 0
        def mock_fun(season, game_code):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise HTTPError("404 Not Found")
            else:
                return pd.DataFrame({
                    'gameCode': [game_code],
                    'season': [season],
                    'data': [1]
                })
        
        with patch('src.euroleague_api.utils.logger') as mock_logger:
            result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
            
            # Should log warning for HTTP error
            mock_logger.warning.assert_called()
            warning_call = mock_logger.warning.call_args[0][0]
            assert "HTTPError" in warning_call
            assert "404 Not Found" in warning_call
            
            # Should return data from the second game only
            assert len(result) == 1
            assert result['gameCode'].iloc[0] == 2
    
    def test_general_exception_handling(self):
        """Test handling of general exceptions during data collection"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1, 2],
            'Phase': ['Regular Season', 'Regular Season'],
            'Round': [1, 1]
        })
        
        call_count = 0
        def mock_fun(season, game_code):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("Some error occurred")
            else:
                return pd.DataFrame({
                    'gameCode': [game_code],
                    'season': [season],
                    'data': [1]
                })
        
        with patch('src.euroleague_api.utils.logger') as mock_logger:
            result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
            
            # Should log warning for general exception
            mock_logger.warning.assert_called()
            warning_call = mock_logger.warning.call_args[0][0]
            assert "Something went wrong" in warning_call
            assert "Some error occurred" in warning_call
            
            # Should return data from the second game only
            assert len(result) == 1
            assert result['gameCode'].iloc[0] == 2
    
    def test_all_failures_return_empty_dataframe(self):
        """Test that all failures result in empty DataFrame"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1, 2],
            'Phase': ['Regular Season', 'Regular Season'],
            'Round': [1, 1]
        })
        
        def mock_fun(season, game_code):
            raise ValueError("Always fails")
        
        with patch('src.euroleague_api.utils.logger'):
            result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0
    
    def test_phase_and_round_insertion(self):
        """Test that Phase and Round are correctly inserted when missing"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1],
            'Phase': ['Playoffs'],
            'Round': [5]
        })
        
        def mock_fun(season, game_code):
            # Return DataFrame without Phase and Round columns
            return pd.DataFrame({
                'gameCode': [game_code],
                'stat1': [10],
                'stat2': [20]
            })
        
        result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
        
        assert 'Phase' in result.columns
        assert 'Round' in result.columns
        assert result['Phase'].iloc[0] == 'Playoffs'
        assert result['Round'].iloc[0] == 5
        
        # Check column order; Phase should be at index 1, Round at index 2
        columns = list(result.columns)
        assert columns[1] == 'Phase'
        assert columns[2] == 'Round'
    
    def test_existing_phase_round_not_overwritten(self):
        """Test that existing Phase and Round columns are not overwritten"""
        game_codes_df = pd.DataFrame({
            'gameCode': [1],
            'Phase': ['Playoffs'],
            'Round': [5]
        })
        
        def mock_fun(season, game_code):
            # Return DataFrame with existing Phase and Round columns
            return pd.DataFrame({
                'gameCode': [game_code],
                'Phase': ['Existing Phase'],
                'Round': [999],
                'stat1': [10]
            })
        
        result = get_data_over_collection_of_games(game_codes_df, 2024, mock_fun)
        
        # Should keep the original values from the function
        assert result['Phase'].iloc[0] == 'Existing Phase'
        assert result['Round'].iloc[0] == 999
