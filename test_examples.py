"""
Test configuration and examples for the EuroLeague API test suite.
This demonstrates how to run tests and what we've built so far.
"""

import sys
import os

# Add the src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_example_tests():
    """Run some example tests to show what we've built."""
    
    print("EuroLeague API Test Suite")
    print("=" * 40)
    
    # Test 1: Basic import functionality
    print("\n1. Testing basic imports...")
    try:
        from euroleague_api.utils import raise_error, get_requests
        from euroleague_api.EuroLeagueData import EuroLeagueData
        from euroleague_api.shot_data import ShotData
        print("   ✓ All core modules imported successfully")
    except ImportError as e:
        print(f"   ✗ Import failed: {e}")
        return False
    
    # Test 2: Test EuroLeagueData initialization
    print("\n2. Testing EuroLeagueData initialization...")
    try:
        # Valid competitions
        el_data = EuroLeagueData(competition="E")
        uc_data = EuroLeagueData(competition="U")
        default_data = EuroLeagueData()
        
        assert el_data.competition == "E"
        assert uc_data.competition == "U" 
        assert default_data.competition == "E"
        print("   ✓ EuroLeagueData initialization tests passed")
        
        # Test invalid competition
        try:
            invalid_data = EuroLeagueData(competition="X")
            print("   ✗ Should have raised ValueError for invalid competition")
            return False
        except ValueError:
            print("   ✓ Invalid competition correctly raises ValueError")
            
    except Exception as e:
        print(f"   ✗ EuroLeagueData test failed: {e}")
        return False
    
    # Test 3: Test raise_error utility
    print("\n3. Testing raise_error utility...")
    try:
        # Valid case - should not raise
        raise_error("valid", "test param", ["valid", "options"])
        print("   ✓ Valid value accepted")
        
        # Invalid case - should raise ValueError
        try:
            raise_error("invalid", "test param", ["valid", "options"])
            print("   ✗ Should have raised ValueError for invalid value")
            return False
        except ValueError:
            print("   ✓ Invalid value correctly raises ValueError")
            
        # Test None handling
        try:
            raise_error(None, "test param", ["valid"], allow_none=False)
            print("   ✗ Should have raised ValueError for None when not allowed")
            return False
        except ValueError:
            print("   ✓ None correctly rejected when not allowed")
            
        # Test None allowed
        raise_error(None, "test param", ["valid"], allow_none=True)
        print("   ✓ None correctly accepted when allowed")
        
    except Exception as e:
        print(f"   ✗ raise_error test failed: {e}")
        return False
    
    # Test 4: Test URL construction
    print("\n4. Testing URL construction...")
    try:
        data = EuroLeagueData(competition="E")
        url = data.make_season_game_url(2023, 1, "boxscore")
        expected = "https://api-live.euroleague.net/v3/competitions/E/seasons/E2023/games/1/boxscore"
        
        assert url == expected, f"Expected {expected}, got {url}"
        print("   ✓ URL construction test passed")
        
    except Exception as e:
        print(f"   ✗ URL construction test failed: {e}")
        return False
    
    # Test 5: Test ShotData initialization
    print("\n5. Testing ShotData initialization...")
    try:
        shot_data = ShotData(competition="E")
        assert shot_data.competition == "E"
        print("   ✓ ShotData initialization test passed")
        
    except Exception as e:
        print(f"   ✗ ShotData test failed: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("✓ All example tests passed!")
    print("\nTest Suite Features:")
    print("- Unit tests for all core components")
    print("- Mocking for API calls to avoid external dependencies")
    print("- Integration test markers for real API calls")
    print("- Error handling and edge case testing")
    print("- Coverage reporting configured")
    print("\nTo run the full test suite:")
    print("  pytest tests/ -v")
    print("\nTo run with coverage:")
    print("  pytest tests/ --cov=euroleague_api --cov-report=html")
    print("\nTo run only unit tests (skip integration):")
    print("  pytest tests/ -m 'not integration'")
    
    return True

if __name__ == "__main__":
    success = run_example_tests()
    if not success:
        sys.exit(1)
