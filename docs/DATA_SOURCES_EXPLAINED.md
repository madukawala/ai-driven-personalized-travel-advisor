# Data Sources & Integration Architecture

## Overview

The application implements two distinct data flows with different levels of integration:

- **Simple Chat** (`/api/chat`): Uses only the local Ollama LLM without external data sources
- **Trip Planning** (`/api/trips`): Integrates multiple third-party APIs and curated travel knowledge

---

## Architecture: Two Different Workflows

The application provides **two different endpoints** with **distinct data integration patterns**:

### 1. Simple Chat Endpoint (`POST /api/chat`)

**Location**: `backend/app/api/routes.py` lines 180-276

**What it does**:
```
User types message → Ollama LLM → Simple response
```

**Data Sources Used**: **NONE**
- ❌ No RAG (Retrieval-Augmented Generation)
- ❌ No Vector Store
- ❌ No travel website data
- ❌ No weather APIs
- ❌ No event APIs
- ❌ No LangGraph workflow

**What it actually does**:
1. Takes your message
2. Looks at recent conversation history (last 10 messages)
3. Sends to Ollama with a simple system prompt: "You are a helpful travel advisor AI"
4. Returns Ollama's response

**Code Evidence** (lines 223-250):
```python
# Just using Ollama with conversation history
from ..rag.ollama_client import OllamaClient
ollama = OllamaClient()

# Simple system prompt - no data retrieval
system_prompt = (
    "You are a helpful travel advisor AI. Help users plan their trips, "
    "provide recommendations, and answer travel-related questions. "
    "Be friendly, informative, and concise."
)

ai_response = await ollama.chat(messages, temperature=0.7)
```

**Result**: Generic AI responses based only on Ollama's training data. No real-time data, no curated knowledge.

---

### 2. Trip Planning Endpoint (`POST /api/trips`)

**Location**: `backend/app/api/routes.py` lines 32-101

**What it does**:
```
User creates trip → LangGraph Workflow → All Agents → External APIs → Vector Store → Comprehensive Itinerary
```

**Data Sources Used**: **ALL OF THEM** ✅

**Code Evidence** (lines 44-59):
```python
# Initialize workflow with ALL agents
workflow = TripPlanningWorkflow()

# Run complete workflow
result = await workflow.run(initial_state)
```

This triggers the **full LangGraph workflow** which includes:

#### A. Real-Time Third-Party APIs (Data Agent)

**Location**: `backend/app/services/data_agent.py`

**API Sources** (as specified in PDF):

1. **OpenWeatherMap API** - Weather forecasts
   ```python
   weather_url = "http://api.openweathermap.org/data/2.5/forecast"
   ```
   - Current weather
   - 5-day forecasts
   - Precipitation chances
   - Temperature highs/lows

2. **Eventbrite API** - Local events
   ```python
   # Fetches local events for the destination
   ```
   - Concerts, festivals
   - Museum exhibitions
   - Local gatherings
   - Holiday events

3. **ExchangeRate API** - Currency conversion
   ```python
   # Currency exchange rates for budget calculations
   ```

4. **Safety Data** - Travel advisories (mocked)
   ```python
   # In production: TravelBriefing API or FCDO Travel Advice
   ```

**Current Status**: Using **mock data** because:
- ⚠️ You saw this warning: `WARNING:app.services.data_agent:Using mock weather data - no API key configured`
- No API keys are configured in `.env`
- App works with realistic mock data

#### B. RAG-Based Knowledge from Travel Websites

**Location**: `backend/app/services/knowledge_agent.py`

**Knowledge Sources** (as specified in PDF):

The `scripts/populate_knowledge_base.py` contains curated content from:

1. **Lonely Planet** ✅
   ```python
   "source_name": "Lonely Planet",
   "source_url": "https://lonelyplanet.com/..."
   ```
   - Museum tips (Paris Louvre, Rome Vatican)
   - Temple guides (Kyoto Fushimi Inari)
   - Practical travel advice

2. **Nomadic Matt** ✅
   ```python
   "source_name": "Nomadic Matt",
   "source_url": "https://nomadicmatt.com/travel-guides/..."
   ```
   - Food markets (Tokyo Tsukiji)
   - Architecture guides (Barcelona Sagrada Familia)
   - Budget tips

3. **TripAdvisor** ✅
   ```python
   "source_name": "TripAdvisor",
   "source_url": "https://tripadvisor.com/..."
   ```
   - Temple guides (Bangkok Grand Palace)
   - Practical tips and warnings

4. **Reddit Travel** ✅
   ```python
   "source_name": "Reddit Travel",
   "source_url": "https://reddit.com/r/travel"
   ```
   - Food markets (London Borough Market)
   - Local experiences

**Current Status**:
- ⚠️ **Vector store is EMPTY** - You saw: `WARNING:app.rag.vector_store:Vector store is empty`
- Data is **ready** in the script but **not loaded**
- Need to run: `python scripts/populate_knowledge_base.py`

**How RAG Works** (when populated):
1. Sample data has 12+ documents with travel knowledge
2. Each document has text, source URL, destination, categories
3. Text is converted to embeddings using Sentence Transformers
4. Stored in FAISS vector database
5. When you plan a trip, relevant snippets are retrieved
6. Top 3-5 most relevant pieces are used to enhance AI responses

#### C. AI Agents & Workflow

**Location**: `backend/app/agents/langgraph_workflow.py`

**4 Specialized Agents**:

1. **Data Agent** → Fetches all real-time data
2. **Risk Agent** → Analyzes budget, weather, crowding risks
3. **Knowledge Agent** → Retrieves RAG-based travel insights
4. **Strategy Agent** → Generates final itinerary using Ollama

**Workflow Steps**:
```
1. fetch_data_node          → Get weather, events, currency
2. analyze_risks_node       → Calculate risk scores
3. retrieve_knowledge_node  → Search vector store for tips
4. check_major_issues_node  → Human-in-the-loop checkpoint
5. generate_itinerary_node  → AI creates day-by-day plan
6. optimize_itinerary_node  → Apply weather/budget adjustments
7. finalize_node           → Generate summary & quality score
```

---

## What's Actually Happening Now

Based on the warnings you're seeing:

### Currently Active:
✅ Ollama LLM (llama2) - Working
✅ LangGraph workflow - Working (simplified mode)
✅ All 4 agents - Working
✅ Backend API - Working
✅ Frontend - Working
✅ Database - Working

### Currently Using Mock Data:
⚠️ Weather data (no OpenWeatherMap API key)
⚠️ Events data (no Eventbrite API key)
⚠️ Currency data (no ExchangeRate API key)

### Currently Empty:
❌ Vector store (FAISS) - Not populated
❌ No travel knowledge from websites

---

## How to Enable Real Data

### 1. Enable RAG (Travel Website Knowledge)

```bash
# From project root
python scripts/populate_knowledge_base.py
```

**What this does**:
- Creates FAISS vector store
- Loads 12+ documents with travel tips from:
  - Lonely Planet
  - Nomadic Matt
  - TripAdvisor
  - Reddit Travel
- Generates embeddings
- Saves to `backend/data/faiss_index/`

**Result**: Trip planning will now include actual curated travel knowledge!

### 2. Enable Real-Time APIs

Edit `backend/.env`:

```env
# Get free API keys from:
OPENWEATHER_API_KEY=your_key_from_openweathermap.org
EVENTBRITE_API_KEY=your_key_from_eventbrite.com
EXCHANGERATE_API_KEY=your_key_from_exchangerate-api.com
```

**Result**: Trip planning will use real weather forecasts, local events, and currency rates!

---

## Data Flow Diagram

### Simple Chat (Current - No External Data)
```
User Message
    ↓
Ollama LLM (local)
    ↓
Generic Response
```

### Trip Planning (Designed - Full Data Integration)
```
User Trip Request
    ↓
LangGraph Workflow
    ↓
┌─────────────────────────────────────────┐
│  Data Agent                              │
│  ├─ OpenWeatherMap API → Weather        │
│  ├─ Eventbrite API → Events             │
│  └─ ExchangeRate API → Currency         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Knowledge Agent                         │
│  ├─ FAISS Vector Store                   │
│  ├─ Lonely Planet content               │
│  ├─ Nomadic Matt content                │
│  ├─ TripAdvisor content                 │
│  └─ Reddit Travel content               │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Risk Agent                              │
│  ├─ Budget analysis                     │
│  ├─ Weather risk scoring                │
│  └─ Crowding analysis                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Strategy Agent                          │
│  └─ Ollama LLM + All Data → Itinerary  │
└─────────────────────────────────────────┘
    ↓
Comprehensive Trip Plan
```

---

## Feature Comparison Matrix

| Feature | Simple Chat | Trip Planning |
|---------|-------------|---------------|
| **Endpoint** | `/api/chat` | `/api/trips` |
| **LLM** | ✅ Ollama | ✅ Ollama |
| **Weather APIs** | ❌ No | ⚠️ Mock (can enable) |
| **Event APIs** | ❌ No | ⚠️ Mock (can enable) |
| **Currency APIs** | ❌ No | ⚠️ Mock (can enable) |
| **RAG / Vector Store** | ❌ No | ❌ Empty (need to populate) |
| **Travel Websites** | ❌ No | ❌ Not loaded yet |
| **LangGraph Workflow** | ❌ No | ✅ Yes (simplified mode) |
| **4 AI Agents** | ❌ No | ✅ Yes |
| **Risk Analysis** | ❌ No | ✅ Yes |
| **Quality Scoring** | ❌ No | ✅ Yes |

---

## Data Source Utilization by Endpoint

### Simple Chat Endpoint

The simple chat endpoint (`/api/chat`) does **NOT** use any third-party data sources. It relies solely on Ollama's built-in knowledge for generating responses.

### Trip Planning Endpoint

The trip planning functionality (`/api/trips` endpoint) is **designed to integrate** the following data sources:
- ✅ Third-party APIs (weather, events, currency)
- ✅ Curated travel knowledge (Lonely Planet, Nomadic Matt, TripAdvisor, Reddit)
- ✅ Multi-agent workflow
- ✅ RAG-based retrieval

**Current Implementation Status**:
The system currently uses mock data due to:
1. API keys not configured (configuration required in `.env` file)
2. Vector store not populated (requires execution of population script)

---

## Configuration Steps

### Enable RAG-Based Travel Knowledge:
```bash
cd /Users/maddy/custom-projects/ai-driven-personalized-travel-advisor
python scripts/populate_knowledge_base.py
```

### Enable Real-Time API Integration:
```bash
# Configure API keys in backend/.env
# Restart backend server to apply changes
```

---

**Documentation Version**: 1.0
**Last Updated**: 2025-11-19
**Status**: Architecture complete, data sources configured, requires population and API key configuration
