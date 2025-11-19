# AI-Driven Personalized Travel Advisor

A comprehensive AI-powered travel planning application that creates personalized, optimized travel itineraries using RAG (Retrieval-Augmented Generation), LangGraph workflow orchestration, and real-time data integration.

## 🌟 Features

### Core Features
- **Natural Language Trip Planning**: Chat with AI to plan trips using conversational interface
- **RAG-Powered Knowledge Retrieval**: Vector database (FAISS) with travel insights from multiple sources
- **Real-Time Data Integration**: Weather forecasts, local events, currency rates, and safety information
- **Risk Analysis**: Budget overrun, weather risks, crowding analysis
- **Human-in-the-Loop Checkpoints**: Approval workflow for major itinerary changes
- **Personalized Recommendations**: Based on user preferences and trip history
- **Quality Scoring**: Trip quality metrics (0-100 scale)

### Optional Enhanced Features
- **Eco-Aware Planning**: Sustainable travel suggestions (public transit, green accommodations)
- **Live Alerts**: Real-time notifications for weather/event changes
- **Trip Quality Benchmarking**: Score trips on comfort, diversity, efficiency
- **Explainable Suggestions**: Detailed reasoning for recommendations
- **Multi-Trip Optimization**: Plan across multiple destinations
- **Voice Input**: Speech-to-text for trip planning

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI** REST API with GraphQL support
- **SQLite** database with SQLAlchemy ORM
- **FAISS** vector store for knowledge retrieval
- **Ollama** local LLM for AI generation
- **LangGraph** workflow orchestration with conditional logic

### Frontend (React + Tailwind CSS)
- **React 18** with Vite
- **Tailwind CSS** for styling
- **React Router** for navigation
- **TanStack Query** for data fetching
- **Recharts** for data visualization

### AI/ML Stack
- **LangGraph**: Multi-step workflow orchestration
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Ollama**: Local LLM (llama2)

## 📋 Prerequisites

- **Python 3.10-3.13** (⚠️ **NOT 3.14+** due to compatibility issues)
- **Node.js 18+**
- **Ollama** (for local LLM)
- **Git**

### ⚠️ Important: Python Version
This application requires **Python 3.10 through 3.13**. Python 3.14+ has compatibility issues with Pydantic V1 and LangGraph dependencies. If you have Python 3.14, the app will run but show warnings. For best experience, use Python 3.13.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-driven-personalized-travel-advisor
```

### 2. Install Ollama

Follow instructions at [ollama.ai](https://ollama.ai) to install Ollama, then:

```bash
ollama pull llama2
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your API keys (optional for testing):
# OPENWEATHER_API_KEY=your_key_here
# EVENTBRITE_API_KEY=your_key_here
# EXCHANGERATE_API_KEY=your_key_here

# Initialize database
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"

# Populate vector store with sample travel knowledge (IMPORTANT!)
cd ..
python scripts/populate_knowledge_base.py
```

**Note**: Populating the vector store is essential! Without it, you'll see "Vector store is empty" warnings and won't get travel knowledge recommendations.

### 4. Start Backend Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 5. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### 6. Start Ollama Server

```bash
# In a new terminal
ollama serve
```

## 📖 Usage

### Planning a Trip via Chat

1. Navigate to the **Chat** page
2. Type your trip request in natural language:
   ```
   "Plan a 5-day food and culture trip to Tokyo in September with a $800 budget"
   ```
3. The AI will:
   - Fetch real-time weather, events, and data
   - Analyze risks (budget, weather, crowding)
   - Retrieve relevant travel knowledge
   - Generate personalized itinerary
   - Request approval for major changes (if needed)

### Using the Trip Form

1. Click "New Trip Form" button
2. Fill in:
   - Destination
   - Start and end dates
   - Budget and currency
   - Interests (food, culture, art, etc.)
3. Click "Create Trip Plan"
4. Review generated itinerary with:
   - Day-by-day schedule
   - Budget breakdown
   - Risk analysis
   - Quality score

### Viewing Trip History

1. Navigate to **My Trips**
2. View all past and planned trips
3. Click on any trip to see detailed itinerary
4. Export or share trip plans

## 🔑 API Keys (Optional)

The app works with mock data, but for real-time data, add these API keys to `.env`:

- **OpenWeatherMap**: Weather forecasts - [Get Key](https://openweathermap.org/api)
- **Eventbrite**: Local events - [Get Key](https://www.eventbrite.com/platform/api)
- **ExchangeRate-API**: Currency conversion - [Get Key](https://www.exchangerate-api.com/)

## 📁 Project Structure

```
ai-driven-personalized-travel-advisor/
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph workflows
│   │   ├── api/             # REST & GraphQL endpoints
│   │   ├── database/        # Database config
│   │   ├── models/          # SQLAlchemy models
│   │   ├── rag/             # RAG system (FAISS, embeddings)
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Agents (Data, Risk, Knowledge, Strategy)
│   │   └── utils/           # Configuration & utilities
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── App.jsx
│   └── package.json
├── data/
│   └── travel_knowledge/    # Knowledge base data
├── scripts/
│   └── populate_knowledge_base.py
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   └── ARCHITECTURE.md
└── README.md
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### End-to-End Tests

```bash
cd tests/e2e
npm run test:e2e
```

## 📊 API Endpoints

### REST API

- `POST /api/trips` - Create new trip
- `GET /api/trips` - List user trips
- `GET /api/trips/{id}` - Get trip details
- `PUT /api/trips/{id}` - Update trip
- `DELETE /api/trips/{id}` - Delete trip
- `POST /api/chat` - Send chat message
- `GET /api/conversations` - List conversations
- `GET /api/users/me` - Get current user
- `POST /api/users/preferences` - Update preferences
- `GET /api/memory/{user_id}` - Get user memory

### GraphQL

Access GraphQL Playground at: `http://localhost:8000/graphql`

Example query:
```graphql
query {
  trips(user_id: 1) {
    id
    destination
    start_date
    end_date
    budget
    quality_score
  }
}
```

## 🤖 AI Workflow

The LangGraph workflow follows these steps:

1. **Fetch Data**: Weather, events, currency, safety info
2. **Analyze Risks**: Budget, weather, crowding analysis
3. **Retrieve Knowledge**: RAG search for travel insights
4. **Check Issues**: Human-in-the-loop checkpoint if risks detected
5. **Generate Itinerary**: AI creates day-by-day plan
6. **Optimize**: Apply weather and budget optimizations
7. **Finalize**: Generate summary and quality score

## 🎨 Customization

### Adding New Travel Knowledge

1. Add content to `data/travel_knowledge/`
2. Run: `python scripts/populate_knowledge_base.py`

### Customizing AI Prompts

Edit prompts in `backend/app/services/strategy_agent.py`

### Adding New Agents

Create new agent in `backend/app/services/` and integrate into LangGraph workflow

## 📝 Environment Variables

### Backend (.env)

```env
# Required
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
DATABASE_URL=sqlite+aiosqlite:///./travel_advisor.db

# Optional API Keys
OPENWEATHER_API_KEY=your_key_here
EVENTBRITE_API_KEY=your_key_here
EXCHANGERATE_API_KEY=your_key_here

# Configuration
FAISS_INDEX_PATH=./data/faiss_index
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_RETRIEVAL_RESULTS=3
SIMILARITY_THRESHOLD=0.7
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Python 3.14 Compatibility Warnings

**Issue**: Warnings about Pydantic V1 and LangGraph compatibility

**Symptoms**:
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14
WARNING:root:LangGraph not fully compatible, using simplified workflow
```

**Solution**:
- **Option 1 (Easy)**: Ignore warnings - app is fully functional
- **Option 2 (Clean)**: Install Python 3.13 using pyenv or brew
  ```bash
  # Using pyenv
  pyenv install 3.13.0
  pyenv local 3.13.0

  # Recreate venv
  cd backend
  rm -rf venv
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

See [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed Python version management.

### Vector Store Empty

**Issue**: "Vector store is empty" warning

**Impact**: No travel knowledge recommendations

**Solution**:
```bash
# Populate the knowledge base (IMPORTANT!)
python scripts/populate_knowledge_base.py

# Verify files created
ls -la backend/data/faiss_index/
```

### Mock Data Warnings

**Issue**: "Using mock weather data" and "Using mock events data" warnings

**Impact**: App uses sample data instead of real-time information

**Solution (Optional)**:
1. Get free API keys from:
   - [OpenWeatherMap](https://openweathermap.org/api)
   - [Eventbrite](https://www.eventbrite.com/platform/api)
   - [ExchangeRate-API](https://www.exchangerate-api.com/)

2. Add to `backend/.env`:
   ```env
   OPENWEATHER_API_KEY=your_key_here
   EVENTBRITE_API_KEY=your_key_here
   EXCHANGERATE_API_KEY=your_key_here
   ```

3. Restart backend server

**Note**: App works perfectly with mock data for testing!

### Ollama Connection Error

**Issue**: "Error calling Ollama"

**Solution**:
```bash
# Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags

# Pull model if needed
ollama pull llama2
```

### Database Errors

**Solution**:
```bash
# Recreate database
rm backend/travel_advisor.db
cd backend
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
```

### Port Already in Use

**Solution**:
```bash
# Backend
lsof -ti:8000 | xargs kill -9

# Frontend
lsof -ti:5173 | xargs kill -9
```

## 🚢 Deployment

### Backend (Docker)

```bash
cd backend
docker build -t travel-advisor-backend .
docker run -p 8000:8000 travel-advisor-backend
```

### Frontend (Vercel/Netlify)

```bash
cd frontend
npm run build
# Deploy 'dist' folder
```

## 📄 License

MIT License - see LICENSE file

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@traveladvisor.com

## 🙏 Acknowledgments

- OpenWeatherMap for weather data
- Ollama for local LLM
- LangChain/LangGraph for workflow orchestration
- Travel blogs and communities for knowledge base content

---

**Built using RAG, LangGraph, FastAPI, and React**
