# Testing Quick Start Guide

## Running Tests - Simple Commands

### Setup (One Time)

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Run All Tests

```bash
# From backend directory with venv activated
PYTHONPATH=. pytest tests/ -v --no-cov
```

### Run Individual Test Files

```bash
# Test agents (Data Agent, Risk Agent)
PYTHONPATH=. pytest tests/test_agents.py -v --no-cov

# Test API endpoints
PYTHONPATH=. pytest tests/test_api.py -v --no-cov

# Test RAG system (Vector Store, Embeddings, Ollama)
PYTHONPATH=. pytest tests/test_rag.py -v --no-cov

# Test LangGraph workflow
PYTHONPATH=. pytest tests/test_workflow.py -v --no-cov

# Test database models
PYTHONPATH=. pytest tests/test_models.py -v --no-cov
```

### Run with Coverage

```bash
# Generate coverage report
PYTHONPATH=. pytest tests/ -v --cov=app --cov-report=html

# Open coverage report in browser
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or
start htmlcov/index.html  # Windows
```

### Run Specific Test

```bash
# Run single test function
PYTHONPATH=. pytest tests/test_agents.py::test_data_agent_weather -v --no-cov

# Run tests matching keyword
PYTHONPATH=. pytest tests/ -k "weather" -v --no-cov
```

### Stop on First Failure

```bash
PYTHONPATH=. pytest tests/ -v --no-cov -x
```

### Show Print Statements

```bash
PYTHONPATH=. pytest tests/ -v --no-cov -s
```

## Test Files Created

| File | Tests | Purpose |
|------|-------|---------|
| `test_agents.py` | 4 | Data & Risk agents |
| `test_api.py` | 15+ | API endpoints |
| `test_rag.py` | 20+ | Vector store, embeddings |
| `test_workflow.py` | 15+ | LangGraph workflow |
| `test_models.py` | 25+ | Database models |

## Expected Output

When tests pass, you'll see:

```
===================== test session starts ======================
collected 4 items

tests/test_agents.py::test_data_agent_weather PASSED   [ 25%]
tests/test_agents.py::test_data_agent_events PASSED    [ 50%]
tests/test_agents.py::test_risk_agent_budget PASSED    [ 75%]
tests/test_agents.py::test_risk_agent_quality_score PASSED [100%]

===================== 4 passed in 0.05s ========================
```

## Troubleshooting

### Module Import Errors

When encountering `ModuleNotFoundError: No module named 'app'`:

```bash
# Make sure to add PYTHONPATH=. before pytest
PYTHONPATH=. pytest tests/ -v --no-cov
```

### Tests Require Ollama

Some tests in `test_rag.py` require Ollama to be running:

```bash
# Start Ollama in another terminal
ollama serve

# Or skip Ollama tests
PYTHONPATH=. pytest tests/ -k "not ollama" -v --no-cov
```

### Import Errors

```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall if needed
pip install -r requirements.txt
```

## Full Documentation

For detailed testing documentation, see: [docs/TESTING.md](docs/TESTING.md)

---

**Quick Command**: `PYTHONPATH=. pytest tests/ -v --no-cov`
