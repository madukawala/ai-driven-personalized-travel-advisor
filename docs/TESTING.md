# Testing Guide

Comprehensive guide for running tests in the AI Travel Advisor application.

## Table of Contents

1. [Test Structure](#test-structure)
2. [Running Tests](#running-tests)
3. [Test Files Overview](#test-files-overview)
4. [Test Coverage](#test-coverage)
5. [Writing New Tests](#writing-new-tests)
6. [Continuous Integration](#continuous-integration)

---

## Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_agents.py       # Agent tests (Data, Risk)
│   ├── test_api.py          # API endpoint tests
│   ├── test_rag.py          # RAG system tests
│   ├── test_workflow.py     # LangGraph workflow tests
│   └── test_models.py       # Database model tests
├── pytest.ini               # Pytest configuration
└── requirements.txt         # Includes testing dependencies
```

---

## Running Tests

### Prerequisites

Ensure you have the backend environment set up:

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run All Tests

```bash
# From backend directory
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test File

```bash
# Test agents only
pytest tests/test_agents.py -v

# Test API endpoints only
pytest tests/test_api.py -v

# Test RAG system only
pytest tests/test_rag.py -v

# Test workflow only
pytest tests/test_workflow.py -v

# Test models only
pytest tests/test_models.py -v
```

### Run Specific Test

```bash
# Run a single test function
pytest tests/test_agents.py::test_data_agent_weather -v

# Run tests matching a pattern
pytest tests/ -k "agent" -v

# Run tests with specific marker
pytest tests/ -m asyncio -v
```

### Run Tests with Output

```bash
# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -v -x

# Run last failed tests
pytest tests/ --lf -v
```

---

## Test Files Overview

### 1. test_agents.py

**Purpose**: Test individual AI agents (Data Agent, Risk Agent)

**Tests**:
- Weather data fetching
- Event data fetching
- Budget risk analysis
- Quality score calculation

**Run**:
```bash
pytest tests/test_agents.py -v
```

**Example Output**:
```
tests/test_agents.py::test_data_agent_weather PASSED
tests/test_agents.py::test_data_agent_events PASSED
tests/test_agents.py::test_risk_agent_budget PASSED
tests/test_agents.py::test_risk_agent_quality_score PASSED
```

### 2. test_api.py

**Purpose**: Test REST API endpoints

**Tests**:
- Health check endpoint
- Trip creation (valid/invalid data)
- Chat endpoint
- Conversation management
- User preferences
- CORS headers

**Run**:
```bash
pytest tests/test_api.py -v
```

**Requirements**:
- Tests use AsyncClient
- No need to run actual server
- Tests are isolated

**Example**:
```bash
# Run only trip tests
pytest tests/test_api.py -k "trip" -v

# Run only chat tests
pytest tests/test_api.py -k "chat" -v
```

### 3. test_rag.py

**Purpose**: Test RAG system (Vector Store, Embeddings, Ollama)

**Tests**:
- Embedding generation
- Vector store operations
- Semantic search
- Ollama text generation
- Knowledge agent retrieval

**Run**:
```bash
pytest tests/test_rag.py -v
```

**Note**: Some tests require Ollama to be running. If Ollama is not available, those tests will be skipped automatically.

**Start Ollama** (if needed):
```bash
# In separate terminal
ollama serve
```

### 4. test_workflow.py

**Purpose**: Test LangGraph workflow orchestration

**Tests**:
- Workflow initialization
- Individual node execution
- Data fetching node
- Risk analysis node
- Knowledge retrieval node
- Itinerary generation node
- Optimization logic
- Error handling

**Run**:
```bash
pytest tests/test_workflow.py -v
```

**Coverage**:
- Tests both graph-based and sequential workflows
- Tests approval logic
- Tests error handling with invalid data

### 5. test_models.py

**Purpose**: Test database models

**Tests**:
- User model creation
- Trip model with itinerary
- Conversation and Message models
- UserPreference model
- UserMemory model
- Model relationships
- Timestamp handling

**Run**:
```bash
pytest tests/test_models.py -v
```

**Note**: These are unit tests and don't require database connection.

---

## Test Coverage

### Generate Coverage Report

```bash
# HTML report (opens in browser)
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

### Terminal Coverage Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Coverage by Module

```bash
# Test coverage for specific module
pytest tests/ --cov=app.services --cov-report=term

# Test coverage for agents
pytest tests/ --cov=app.agents --cov-report=term

# Test coverage for RAG
pytest tests/ --cov=app.rag --cov-report=term
```

### Expected Coverage

| Module | Target Coverage | Current Status |
|--------|----------------|----------------|
| app.services | 80%+ | Good |
| app.agents | 70%+ | Good |
| app.rag | 75%+ | Good |
| app.api | 85%+ | Good |
| app.models | 90%+ | Excellent |

---

## Running Tests - Quick Reference

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app

# Run specific file
pytest tests/test_agents.py -v

# Run specific test
pytest tests/test_agents.py::test_data_agent_weather -v

# Run tests matching pattern
pytest tests/ -k "weather" -v

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -s

# Run in parallel (faster)
pytest tests/ -n auto
```

### Test Markers

```bash
# Run only async tests
pytest tests/ -m asyncio -v

# Skip slow tests
pytest tests/ -m "not slow" -v
```

---

## Test Environment Setup

### Environment Variables for Testing

Create `backend/.env.test` (optional):

```env
# Test environment
ENVIRONMENT=test
DEBUG=True

# Test database (optional - tests use in-memory by default)
DATABASE_URL=sqlite+aiosqlite:///:memory:

# Ollama for tests (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vector store (optional)
FAISS_INDEX_PATH=./tests/test_data/faiss_index
```

### Mocking External Services

Tests automatically mock:
- ✅ Weather API calls (uses mock data)
- ✅ Events API calls (uses mock data)
- ✅ Currency API calls (uses mock data)
- ⚠️ Ollama calls (skipped if not available)

---

## Writing New Tests

### Test File Template

```python
"""
Test cases for [component name]
Run with: pytest tests/test_[name].py -v
"""

import pytest
from datetime import datetime


@pytest.fixture
def sample_data():
    """Create sample test data"""
    return {"key": "value"}


def test_something():
    """Test description"""
    # Arrange
    expected = "result"

    # Act
    result = some_function()

    # Assert
    assert result == expected


@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    result = await async_function()
    assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Best Practices

1. **Naming Convention**:
   - File: `test_[module_name].py`
   - Function: `test_[what_it_tests]`
   - Use descriptive names

2. **Fixtures**:
   - Use fixtures for reusable test data
   - Use `@pytest.fixture` decorator
   - Scope: function (default), class, module, session

3. **Async Tests**:
   - Use `@pytest.mark.asyncio` for async tests
   - `pytest-asyncio` is required (already in requirements.txt)

4. **Assertions**:
   - Use clear, specific assertions
   - Test one thing per test function
   - Use descriptive error messages

5. **Mocking**:
   - Mock external dependencies
   - Use `pytest-mock` or `unittest.mock`
   - Don't mock what you're testing

---

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.13'

    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt

    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./backend/coverage.xml
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Ensure you're in backend directory
cd backend

# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Async Test Failures

**Problem**: `RuntimeError: Event loop is closed`

**Solution**:
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Check pytest.ini has asyncio configuration
cat pytest.ini
```

#### 3. Ollama Tests Failing

**Problem**: Tests requiring Ollama are failing

**Solution**:
```bash
# Start Ollama server
ollama serve

# Or skip Ollama tests
pytest tests/ -v -k "not ollama"
```

#### 4. Database Connection Errors

**Problem**: SQLAlchemy connection errors

**Solution**:
Tests use in-memory database by default. If you see connection errors:
```bash
# Ensure aiosqlite is installed
pip install aiosqlite

# Check DATABASE_URL in pytest.ini or .env.test
```

#### 5. Coverage Not Working

**Problem**: Coverage report not generated

**Solution**:
```bash
# Install coverage plugin
pip install pytest-cov

# Use correct syntax
pytest tests/ --cov=app --cov-report=html
```

---

## Test Statistics

### Current Test Count

```bash
# Count all tests
pytest tests/ --collect-only | grep "test session starts"

# Expected:
# - test_agents.py: 4 tests
# - test_api.py: 15+ tests
# - test_rag.py: 20+ tests
# - test_workflow.py: 15+ tests
# - test_models.py: 25+ tests
# Total: 75+ tests
```

### Test Execution Time

```bash
# Show slowest tests
pytest tests/ --durations=10

# Set timeout for slow tests
pytest tests/ --timeout=30
```

---

## Advanced Testing

### Parameterized Tests

```python
@pytest.mark.parametrize("destination,budget,expected", [
    ("Tokyo", 800, "success"),
    ("Paris", 1000, "success"),
    ("London", 500, "budget_warning"),
])
def test_trip_planning(destination, budget, expected):
    result = plan_trip(destination, budget)
    assert result.status == expected
```

### Fixtures with Scope

```python
@pytest.fixture(scope="module")
def database():
    """Create database once per module"""
    db = create_database()
    yield db
    db.close()
```

### Mocking External Calls

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_with_mock():
    with patch('app.services.data_agent.httpx.AsyncClient') as mock:
        mock.return_value.get = AsyncMock(return_value={"data": "test"})
        result = await fetch_data()
        assert result == {"data": "test"}
```

---

## Quick Commands Cheat Sheet

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific file
pytest tests/test_agents.py -v

# Run specific test
pytest tests/test_agents.py::test_data_agent_weather -v

# Run tests matching keyword
pytest tests/ -k "weather" -v

# Stop on first failure
pytest tests/ -x -v

# Show print output
pytest tests/ -s -v

# Run in parallel
pytest tests/ -n auto

# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

---

## Summary

✅ **5 Test Files** covering all major components
✅ **75+ Test Cases** for comprehensive coverage
✅ **Async Support** for testing async functions
✅ **Mocking** for external dependencies
✅ **Coverage Reports** for tracking test coverage
✅ **CI/CD Ready** for automated testing

**Next Steps**:
1. Run all tests: `pytest tests/ -v`
2. Check coverage: `pytest tests/ --cov=app --cov-report=html`
3. Add new tests as you develop features
4. Maintain >80% coverage for critical modules

---

**Last Updated**: 2025-11-19
**Version**: 1.0.0
