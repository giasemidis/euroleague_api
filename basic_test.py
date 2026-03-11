"""
Basic test to verify the testing setup works.
"""

def test_basic_import():
    """Test that we can import the euroleague_api modules."""
    try:
        from euroleague_api import utils
        assert hasattr(utils, 'raise_error')
        assert hasattr(utils, 'get_requests')
        print("✓ Basic import test passed")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_raise_error_function():
    """Test the raise_error utility function."""
    from euroleague_api.utils import raise_error
    
    # Test valid case - should not raise
    try:
        raise_error("valid", "test param", ["valid", "options"])
        print("✓ raise_error valid case passed")
    except Exception as e:
        print(f"✗ raise_error valid case failed: {e}")
        return False
    
    # Test invalid case - should raise ValueError
    try:
        raise_error("invalid", "test param", ["valid", "options"])
        print("✗ raise_error should have raised ValueError")
        return False
    except ValueError:
        print("✓ raise_error invalid case correctly raised ValueError")
        return True
    except Exception as e:
        print(f"✗ raise_error raised unexpected exception: {e}")
        return False

if __name__ == "__main__":
    print("Running basic tests...")
    test1 = test_basic_import()
    test2 = test_raise_error_function()
    
    if test1 and test2:
        print("\n✓ All basic tests passed!")
    else:
        print("\n✗ Some tests failed!")
