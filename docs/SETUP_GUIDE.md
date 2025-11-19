# Complete Setup Guide

This comprehensive guide will walk you through setting up the AI-Driven Personalized Travel Advisor application on your local machine or deploying it to a server.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites Installation](#prerequisites-installation)
3. [Project Setup](#project-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Database Initialization](#database-initialization)
7. [Vector Store Setup](#vector-store-setup)
8. [Running the Application](#running-the-application)
9. [Production Deployment](#production-deployment)
10. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+
- **RAM**: 8GB (16GB recommended)
- **Storage**: 5GB free space
- **CPU**: 4 cores recommended

### Software Requirements
- **Python**: 3.10 to 3.13 (⚠️ **NOT 3.14+** - see compatibility notes below)
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **Ollama**: Latest version
- **Git**: 2.30 or higher

#### ⚠️ Python Version Compatibility Note
**IMPORTANT**: This application requires Python 3.10 through 3.13. **Python 3.14+ is NOT compatible** due to:
- Pydantic V1 compatibility issues with Python 3.14+
- LangGraph dependency conflicts

If you have Python 3.14 installed, you have two options:
1. **Recommended**: Install Python 3.13 alongside (using pyenv or similar)
2. Accept warnings (app will run but with compatibility warnings)

---

## Prerequisites Installation

### 1. Install Python 3.10-3.13

#### macOS
```bash
# Install Python 3.13 (recommended)
brew install python@3.13

# Or use pyenv for version management
brew install pyenv
pyenv install 3.13.0
pyenv global 3.13.0
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip

# Or install specific version
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv
```

#### Windows
Download Python 3.13 from [python.org](https://www.python.org/downloads/) and install.

Verify installation:
```bash
python --version  # Should show 3.10-3.13 (NOT 3.14+)
```

⚠️ **If you see Python 3.14.0**, the app will run but with compatibility warnings. Consider downgrading to 3.13 for best experience.

### 2. Install Node.js and npm

#### macOS
```bash
brew install node
```

#### Ubuntu/Debian
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Windows
Download from [nodejs.org](https://nodejs.org/) and install.

Verify installation:
```bash
node --version  # Should show v18 or higher
npm --version   # Should show v9 or higher
```

### 3. Install Ollama

#### macOS/Linux
```bash
curl https://ollama.ai/install.sh | sh
```

#### Windows
Download from [ollama.ai](https://ollama.ai/download/windows) and install.

Pull the required model:
```bash
ollama pull llama2
```

Verify installation:
```bash
ollama --version
ollama list  # Should show llama2
```

### 4. Install Git (if not already installed)

#### macOS
```bash
brew install git
```

#### Ubuntu/Debian
```bash
sudo apt install git
```

#### Windows
Download from [git-scm.com](https://git-scm.com/) and install.

---

## Project Setup

### 1. Clone the Repository

```bash
# Clone the project
git clone <repository-url>
cd ai-driven-personalized-travel-advisor

# Or if you have a ZIP file
unzip ai-driven-personalized-travel-advisor.zip
cd ai-driven-personalized-travel-advisor
```

### 2. Project Structure Overview

```
ai-driven-personalized-travel-advisor/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── scripts/          # Utility scripts
├── docs/             # Documentation
├── data/             # Data files
└── README.md
```

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Python Virtual Environment

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Upgrade pip

```bash
pip install --upgrade pip
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- LangGraph
- FAISS
- Sentence Transformers
- Ollama client
- And other dependencies

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file
nano .env  # or use your preferred editor
```

#### Required Environment Variables

```env
# Application
APP_NAME=AI Travel Advisor
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite+aiosqlite:///./travel_advisor.db

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vector Store
FAISS_INDEX_PATH=./data/faiss_index
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# RAG Configuration
MAX_RETRIEVAL_RESULTS=3
SIMILARITY_THRESHOLD=0.7

# Agent Configuration
WEATHER_RISK_THRESHOLD=0.7
BUDGET_OVERRUN_THRESHOLD=1.2
DEFAULT_TRIP_DAYS=5
```

#### Optional API Keys (for real-time data)

```env
# Weather Data (optional)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Events Data (optional)
EVENTBRITE_API_KEY=your_eventbrite_api_key_here

# Currency Exchange (optional)
EXCHANGERATE_API_KEY=your_exchangerate_api_key_here
```

**Note**: The application works with mock data if API keys are not provided.

### 6. Get API Keys (Optional)

#### OpenWeatherMap
1. Visit [openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for free account
3. Generate API key
4. Add to `.env` file

#### Eventbrite
1. Visit [eventbrite.com/platform/api](https://www.eventbrite.com/platform/api)
2. Create app and get API key
3. Add to `.env` file

#### ExchangeRate-API
1. Visit [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Sign up for free account
3. Get API key
4. Add to `.env` file

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
# From project root
cd frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This will install:
- React
- React Router
- TanStack Query
- Tailwind CSS
- Recharts
- And other dependencies

### 3. Configure Environment (Optional)

```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

---

## Database Initialization

### 1. Start Ollama Server (Required)

```bash
# In a new terminal
ollama serve
```

Keep this terminal open.

### 2. Initialize Database

```bash
# From backend directory with venv activated
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run database initialization
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
```

This creates:
- SQLite database file: `travel_advisor.db`
- All required tables (users, trips, conversations, etc.)

### 3. Verify Database Creation

```bash
# Check if database file exists
ls -la travel_advisor.db

# You should see a file with size > 0
```

---

## Vector Store Setup

### 1. Populate Knowledge Base

```bash
# From project root
cd scripts

# Run the population script
python populate_knowledge_base.py
```

This will:
- Load sample travel knowledge data
- Generate embeddings using Sentence Transformers
- Create FAISS index
- Save to `backend/data/faiss_index`

Expected output:
```
Initializing vector store...
Adding 12 documents to vector store...
Successfully added 12 documents
Saving vector store...
✅ Vector store populated successfully!

Testing search functionality...
Found 3 results for 'food in Tokyo':
1. Tokyo - Nomadic Matt
   Score: 0.8523
   Text: Tokyo's Tsukiji Outer Market is best visited...
```

### 2. Verify Vector Store

```bash
# Check if FAISS index files exist
ls -la backend/data/faiss_index.*

# You should see:
# faiss_index.faiss
# faiss_index.pkl
```

---

## Running the Application

### 1. Start Ollama (if not already running)

```bash
# In terminal 1
ollama serve
```

### 2. Start Backend Server

```bash
# In terminal 2
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Starting AI Travel Advisor API...
INFO:     Database initialized
INFO:     Vector store initialized with 12 documents
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Backend available at: **http://localhost:8000**

### 3. Start Frontend Development Server

```bash
# In terminal 3
cd frontend
npm run dev
```

Expected output:
```
VITE v5.0.8  ready in 523 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

Frontend available at: **http://localhost:5173**

### 4. Expected Warnings (Normal Operation)

When starting the backend, you may see these warnings - **they are normal and the app will work**:

```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```
- **Cause**: Using Python 3.14 with Pydantic V1
- **Impact**: App works but with warnings
- **Fix**: Use Python 3.10-3.13 for clean startup

```
WARNING:root:LangGraph not fully compatible, using simplified workflow
```
- **Cause**: LangGraph MemorySaver import issue
- **Impact**: Uses simplified sequential workflow (app still works normally)
- **Fix**: No action needed - this is a known compatibility fallback

```
WARNING:app.rag.vector_store:Vector store is empty
```
- **Cause**: Knowledge base not populated
- **Impact**: No travel knowledge recommendations
- **Fix**: Run `python scripts/populate_knowledge_base.py`

```
WARNING:app.services.data_agent:Using mock weather data - no API key configured
WARNING:app.services.data_agent:Using mock events data - no API key configured
```
- **Cause**: No API keys in .env file
- **Impact**: Uses mock data instead of real-time data
- **Fix**: Add API keys to `.env` (optional - app works with mock data)

```
WARNING:app.agents.langgraph_workflow:Using simplified sequential workflow (LangGraph not available)
```
- **Cause**: LangGraph compatibility mode
- **Impact**: Trip planning uses sequential workflow instead of graph-based
- **Fix**: No action needed - functionality is equivalent

### 5. Verify Application is Running

Open browser and navigate to:
- Frontend: **http://localhost:5173**
- Backend API Docs: **http://localhost:8000/docs**
- GraphQL Playground: **http://localhost:8000/graphql**

---

## Testing the Application

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Test Frontend Loading

Open **http://localhost:5173** in browser. You should see:
- Homepage with "AI-Powered Travel Planning" heading
- Navigation menu (Chat, My Trips, Profile)
- Features section

### 3. Test Chat Functionality

1. Click "Start Planning" or navigate to "Chat"
2. Type: "Plan a 5-day trip to Tokyo with $800 budget"
3. Press Send
4. AI should respond (may take 10-30 seconds first time)

### 4. Test Trip Creation

1. Click "New Trip Form"
2. Fill in:
   - Destination: Tokyo
   - Start Date: (future date)
   - End Date: (5 days later)
   - Budget: 800
   - Interests: Select food, culture
3. Click "Create Trip Plan"
4. Should see trip result with itinerary

---

## Production Deployment

### Backend Deployment (Docker)

1. Create Dockerfile (already included in project):

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run:

```bash
cd backend
docker build -t travel-advisor-backend .
docker run -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  travel-advisor-backend
```

### Frontend Deployment (Vercel/Netlify)

```bash
cd frontend

# Build production version
npm run build

# Deploy 'dist' folder to hosting service
# For Vercel:
vercel deploy

# For Netlify:
netlify deploy --prod
```

---

## Troubleshooting

### Issue: Python 3.14 Compatibility Warnings

**Symptoms**:
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
WARNING:root:LangGraph not fully compatible, using simplified workflow
```

**Impact**: App runs successfully but shows warnings at startup. Uses simplified workflow instead of full LangGraph.

**Solutions**:

**Option 1: Continue with warnings (easiest)**
- No action needed - app is fully functional
- Warnings are informational only
- All features work normally

**Option 2: Install Python 3.13 (recommended for clean experience)**

Using pyenv (macOS/Linux):
```bash
# Install pyenv if not already installed
curl https://pyenv.run | bash

# Install Python 3.13
pyenv install 3.13.0
pyenv local 3.13.0

# Recreate virtual environment
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Using Homebrew (macOS):
```bash
# Install Python 3.13
brew install python@3.13

# Create venv with specific version
cd backend
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows:
```bash
# Download and install Python 3.13 from python.org
# Then recreate virtual environment
cd backend
rmdir /s venv
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Ollama connection error"

**Symptoms**: Error in backend logs about connecting to Ollama

**Solutions**:
```bash
# 1. Check if Ollama is running
curl http://localhost:11434/api/tags

# 2. Start Ollama
ollama serve

# 3. Verify model is pulled
ollama list

# 4. Pull model if missing
ollama pull llama2
```

### Issue: "Vector store is empty"

**Symptoms**: "Vector store is empty" warning in logs

**Solution**:
```bash
cd scripts
python populate_knowledge_base.py
```

### Issue: "Database initialization failed"

**Symptoms**: Error creating database tables

**Solutions**:
```bash
# 1. Delete existing database
rm backend/travel_advisor.db

# 2. Reinstall dependencies
cd backend
pip install --upgrade -r requirements.txt

# 3. Reinitialize
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
```

### Issue: "Port already in use"

**Symptoms**: "Address already in use" error

**Solutions**:

```bash
# Find and kill process on port 8000 (backend)
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (port 5173)
# macOS/Linux:
lsof -ti:5173 | xargs kill -9

# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Issue: "Module not found" errors

**Symptoms**: Python import errors

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify installation
pip list
```

### Issue: Frontend build fails

**Symptoms**: npm build errors

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Update npm
npm install -g npm@latest
```

### Issue: Slow AI responses

**Symptoms**: Chat responses take >60 seconds

**Solutions**:
- Ensure Ollama is using GPU (if available)
- Use smaller model: `ollama pull llama2:7b`
- Increase timeout in `backend/app/rag/ollama_client.py`

### Issue: API keys not working

**Symptoms**: Still seeing mock data despite adding API keys

**Solutions**:
```bash
# 1. Verify .env file is in correct location
ls -la backend/.env

# 2. Restart backend server after updating .env
# Stop server (Ctrl+C) and restart

# 3. Check API key format (no quotes needed)
# Correct: OPENWEATHER_API_KEY=abc123
# Wrong: OPENWEATHER_API_KEY="abc123"
```

---

## Verification Checklist

Before considering setup complete, verify:

- [ ] Ollama server is running (`ollama list` shows llama2)
- [ ] Backend server starts (warnings are OK - see "Expected Warnings" section)
- [ ] Frontend loads in browser
- [ ] Database file exists (`backend/travel_advisor.db`)
- [ ] **Vector store populated** - Run `python scripts/populate_knowledge_base.py` if you see "Vector store is empty" warning
- [ ] Vector store files exist (`backend/data/faiss_index/faiss_index.faiss`, `faiss_index.pkl`)
- [ ] Chat interface responds to messages
- [ ] Trip creation works via form
- [ ] API documentation accessible at `http://localhost:8000/docs`
- [ ] GraphQL playground accessible at `http://localhost:8000/graphql`

**Note**: If you see warnings about Python 3.14, Pydantic, or LangGraph - this is normal! The app works perfectly fine with these warnings.

---

## Next Steps

After setup:

1. **Explore the Application**: Try creating trips with different parameters
2. **Read API Documentation**: Visit `/docs` for API reference
3. **Customize Knowledge Base**: Add your own travel insights
4. **Configure API Keys**: Enable real-time data integration
5. **Run Tests**: Execute test suites to verify functionality

---

## Support

If you encounter issues not covered here:

1. Check the main [README.md](../README.md)
2. Review [API Documentation](API_DOCUMENTATION.md)
3. Check [Architecture Guide](ARCHITECTURE.md)
4. Search existing GitHub issues
5. Create new issue with:
   - Operating system
   - Python/Node versions
   - Error messages
   - Steps to reproduce

---

**Setup Complete - Application Ready for Use**
