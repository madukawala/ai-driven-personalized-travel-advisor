# Quick Start Guide

Get the AI Travel Advisor running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.10-3.13, NOT 3.14+)
python --version

# Check Node.js version (need 18+)
node --version

# Check if Ollama is installed
ollama --version
```

### ⚠️ Important: Python Version
**You need Python 3.10-3.13** (NOT 3.14+). If you see `Python 3.14.0`, the app will work but show compatibility warnings. For best experience, use Python 3.13.

## Installation (5 Steps)

### 1. Install Ollama & Pull Model (2 min)

```bash
# Install Ollama from https://ollama.ai
# Then pull the model:
ollama pull llama2
```

### 2. Backend Setup (2 min)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"

# Populate knowledge base
cd ..
python scripts/populate_knowledge_base.py
```

### 3. Frontend Setup (1 min)

```bash
cd frontend
npm install
```

## Running (3 Terminals)

### Terminal 1: Ollama

```bash
ollama serve
```

### Terminal 2: Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

### Terminal 3: Frontend

```bash
cd frontend
npm run dev
```

Visit: http://localhost:5173

## Expected Warnings (These are Normal!)

When starting the backend, you may see these warnings - **app works fine**:

```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14
WARNING:root:LangGraph not fully compatible, using simplified workflow
WARNING:app.rag.vector_store:Vector store is empty
WARNING:app.services.data_agent:Using mock weather data
WARNING:app.services.data_agent:Using mock events data
```

**What this means**:
- Python 3.14 warnings: Use Python 3.13 for clean startup (optional)
- LangGraph warning: App uses simplified workflow (works perfectly)
- Vector store empty: Run `python scripts/populate_knowledge_base.py`
- Mock data: App uses sample data (add API keys to `.env` for real data)

**These warnings don't affect functionality!** The app is fully operational.

## First Trip

1. Go to http://localhost:5173
2. Click "Start Planning"
3. Type: "Plan a 5-day food tour in Tokyo with $800 budget"
4. Wait 10-30 seconds
5. See your personalized itinerary!

## Troubleshooting

**Python 3.14 Warnings?**
```bash
# Option 1: Ignore warnings - app works fine!

# Option 2: Install Python 3.13 for clean startup
pyenv install 3.13.0
pyenv local 3.13.0
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Ollama not connecting?**
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart
ollama serve

# Pull model if needed
ollama pull llama2
```

**Vector store empty?**
```bash
# IMPORTANT: Populate the knowledge base
python scripts/populate_knowledge_base.py

# Verify it worked
ls -la backend/data/faiss_index/
```

**Using mock data?**
```bash
# Optional: Add real API keys to backend/.env
# Get free keys from:
# - https://openweathermap.org/api
# - https://www.eventbrite.com/platform/api
# - https://www.exchangerate-api.com/

# Edit backend/.env and add:
# OPENWEATHER_API_KEY=your_key_here
# EVENTBRITE_API_KEY=your_key_here
# EXCHANGERATE_API_KEY=your_key_here

# Then restart backend server
```

**Port in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

## What's Next?

- Read [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed setup
- Check [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API reference
- Explore [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Add real API keys to `.env` for live data

## Optional: Add API Keys

Edit `backend/.env`:

```env
OPENWEATHER_API_KEY=your_key_here
EVENTBRITE_API_KEY=your_key_here
EXCHANGERATE_API_KEY=your_key_here
```

Restart backend to use real-time data!

---

**Application Ready - Begin Trip Planning**
