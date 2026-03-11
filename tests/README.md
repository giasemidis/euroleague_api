
## Test Structure

```
tests/
├── __init__.py                 # Test package marker
├── conftest.py                 # Shared fixtures and utilities
├── test_euroleague_data.py     # Tests for base EuroLeagueData class
├── test_utils.py               # Tests for utility functions
├── test_shot_data.py           # Tests for ShotData class
├── test_boxscore_data.py       # Tests for BoxScoreData class
└── README.md                   
```

### Unit Tests
- **Scope**: Test individual functions and methods in isolation
- **Mocking**: Use mocked API responses to avoid external dependencies
- **Marker**: `@pytest.mark.unit`

### Integration Tests  
- **Scope**: Test real API interactions
- **Marker**: `@pytest.mark.integration`

## Running Tests

### Prerequisites
```bash
# Install the package in development mode
pip install -e .[dev]

# Or manually
pip install pytest pytest-cov pytest-mock responses
```

### Basic Test Execution

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_utils.py -v

# Run specific test class
pytest tests/test_utils.py::TestRaiseError -v

# Run specific test method
pytest tests/test_utils.py::TestRaiseError::test_raise_error_valid_value -v
```

### Test Filtering

```bash
# Run only unit tests (exclude integration tests)
pytest tests/ -m "not integration"

# Run only integration tests
pytest tests/ -m "integration"

# Run fast tests only (exclude slow tests)
pytest tests/ -m "not slow"

# Combine markers
pytest tests/ -m "integration and not slow"
```

### Coverage Reporting

```bash
# Run tests with coverage
pytest tests/ --cov=euroleague_api

# Generate HTML coverage report
pytest tests/ --cov=euroleague_api --cov-report=html

# Generate XML coverage report (for CI/CD)
pytest tests/ --cov=euroleague_api --cov-report=xml

# Set coverage threshold
pytest tests/ --cov=euroleague_api --cov-fail-under=80
```

### Debug Mode

```bash
# Run with Python debugger on failures
pytest tests/ --pdb

# Run with detailed output
pytest tests/ -vvv

# Run only failed tests from last run
pytest tests/ --lf
```
