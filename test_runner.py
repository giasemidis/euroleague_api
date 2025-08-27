#!/usr/bin/env python3
"""
Simple test runner to verify our test setup
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    # Import test modules
    from src.euroleague_api.utils import raise_error
    print("✓ Successfully imported utils module")
    
    # Test the raise_error function
    try:
        raise_error("valid", "test param", ["valid", "options"])
        print("✓ raise_error function works correctly")
    except Exception as e:
        print(f"✗ raise_error test failed: {e}")
    
    # Try importing test files
    try:
        import tests.test_utils
        print("✓ Successfully imported test_utils")
    except Exception as e:
        print(f"✗ Failed to import test_utils: {e}")
    
    # Try running a specific test function
    try:
        from tests.test_utils import TestRaiseError
        test_instance = TestRaiseError()
        test_instance.test_raise_error_valid_value()
        print("✓ Successfully ran test_raise_error_valid_value")
    except Exception as e:
        print(f"✗ Failed to run test: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
