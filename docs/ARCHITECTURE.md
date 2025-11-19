# System Architecture

Comprehensive architecture documentation for the AI-Driven Personalized Travel Advisor.

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [LangGraph Workflow](#langgraph-workflow)
6. [RAG System](#rag-system)
7. [Database Schema](#database-schema)
8. [Security Considerations](#security-considerations)

---

## Overview

The system is built with a modern, microservice-oriented architecture using:
- **Backend**: FastAPI with async/await patterns
- **Frontend**: React with modern hooks and state management
- **AI/ML**: LangGraph + RAG (FAISS + Ollama)
- **Database**: SQLite with SQLAlchemy ORM
- **Caching**: In-memory for vector store

### Design Principles

1. **Modularity**: Independent agents for different concerns
2. **Scalability**: Async operations, stateless design
3. **Observability**: Comprehensive logging and monitoring
4. **Reliability**: Error handling, fallback mechanisms
5. **Maintainability**: Clear separation of concerns

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Chat   │  │  Trips   │  │ Profile  │  │  Visuals │       │
│  │   Page   │  │  Page    │  │  Page    │  │Components│       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       └─────────────┴──────────────┴─────────────┘              │
│                         │                                        │
│                    API Client                                    │
└─────────────────────────┼────────────────────────────────────────┘
                          │ HTTP/GraphQL
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API Layer                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │  │  REST    │  │ GraphQL  │  │   CORS   │             │   │
│  │  │Endpoints │  │ Resolver │  │Middleware│             │   │
│  │  └────┬─────┘  └────┬─────┘  └──────────┘             │   │
│  └───────┼─────────────┼──────────────────────────────────┘   │
│          └─────────────┴───────────────┐                       │
│                                         ▼                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LangGraph Workflow                         │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐      │   │
│  │  │  Fetch │→ │ Risk   │→ │Knowledge│→│Strategy│      │   │
│  │  │  Data  │  │Analysis│  │Retrieval│  │  Gen   │      │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│          │              │             │             │           │
│          ▼              ▼             ▼             ▼           │
│  ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │    Data    │  │   Risk   │  │Knowledge │  │ Strategy │    │
│  │   Agent    │  │  Agent   │  │  Agent   │  │  Agent   │    │
│  └────────────┘  └──────────┘  └──────────┘  └──────────┘    │
│         │                             │             │          │
│         ▼                             ▼             │          │
│  ┌────────────┐              ┌────────────┐        │          │
│  │  External  │              │    RAG     │        │          │
│  │    APIs    │              │   System   │        │          │
│  │(Weather,   │              │ ┌────────┐ │        │          │
│  │ Events,    │              │ │ FAISS  │ │        │          │
│  │ Currency)  │              │ │  DB    │ │        │          │
│  └────────────┘              │ └────────┘ │        │          │
│                              │ ┌────────┐ │        │          │
│                              │ │Sentence│ │        │          │
│                              │ │Transf. │ │        │          │
│                              │ └────────┘ │        │          │
│                              └────────────┘        │          │
│                                                    ▼          │
│  ┌────────────┐              ┌────────────┐  ┌────────────┐  │
│  │  SQLite    │              │   Ollama   │  │   Logs     │  │
│  │  Database  │              │    LLM     │  │  & Metrics │  │
│  └────────────┘              └────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Frontend Layer

#### React Application
- **Router**: React Router v6 for navigation
- **State**: TanStack Query for server state
- **Styling**: Tailwind CSS for utility-first styling
- **Charts**: Recharts for data visualization

#### Key Pages
1. **HomePage**: Landing page with features
2. **ChatPage**: Conversational trip planning
3. **TripsPage**: List of user trips
4. **TripDetailPage**: Detailed itinerary view

#### Components
- **ChatMessage**: Message display with formatting
- **TripPlanForm**: Form for structured trip input
- **TripResultCard**: Trip summary with visualizations
- **Visualizations**: Pie charts, timelines, heatmaps

### Backend Layer

#### FastAPI Application
- **Async**: Full async/await support
- **Validation**: Pydantic models
- **Documentation**: Auto-generated OpenAPI docs
- **CORS**: Configured for frontend access

#### API Routes (`app/api/routes.py`)
- Trip management (CRUD)
- Chat interactions
- User preferences
- Memory retrieval

#### GraphQL Schema (`app/api/graphql_schema.py`)
- Strawberry GraphQL
- Type-safe queries and mutations
- Real-time subscriptions (future)

### AI Layer

#### Agents (`app/services/`)

**1. Data Agent** (`data_agent.py`)
- Fetches weather from OpenWeatherMap
- Gets local events from Eventbrite
- Retrieves currency exchange rates
- Collects safety information
- **Pattern**: Parallel async requests with fallback to mock data

**2. Risk Agent** (`risk_agent.py`)
- Analyzes budget overrun risks
- Evaluates weather impacts
- Assesses crowding/holiday risks
- Calculates trip quality score (0-100)
- **Pattern**: Rule-based scoring with weighted factors

**3. Knowledge Agent** (`knowledge_agent.py`)
- Searches vector store (FAISS)
- Retrieves top-K relevant documents
- Performs sentiment analysis
- Filters by location/activity
- **Pattern**: Semantic search with re-ranking

**4. Strategy Agent** (`strategy_agent.py`)
- Generates day-by-day itineraries
- Combines all data sources
- Creates activity schedules
- Provides recommendations
- **Pattern**: LLM-based generation with structured output

#### LangGraph Workflow (`app/agents/langgraph_workflow.py`)

State machine for trip planning:
```python
┌──────────┐
│  Start   │
└────┬─────┘
     ▼
┌──────────┐
│Fetch Data│  → Weather, Events, Currency, Safety
└────┬─────┘
     ▼
┌──────────┐
│Analyze   │  → Budget, Weather, Crowding Risks
│ Risks    │
└────┬─────┘
     ▼
┌──────────┐
│Retrieve  │  → RAG Search for Travel Knowledge
│Knowledge │
└────┬─────┘
     ▼
┌──────────┐
│  Check   │  → Human-in-the-Loop Checkpoint
│  Issues  │  → If high risk, request approval
└────┬─────┘
     ▼
┌──────────┐
│Generate  │  → LLM creates itinerary
│Itinerary │
└────┬─────┘
     ▼
┌──────────┐
│Optimize  │  → Apply weather/budget optimizations
└────┬─────┘
     ▼
┌──────────┐
│Finalize  │  → Generate summary
└────┬─────┘
     ▼
┌──────────┐
│   End    │
└──────────┘
```

#### RAG System (`app/rag/`)

**Vector Store** (`vector_store.py`)
- FAISS for similarity search
- IndexFlatL2 for exact search
- Pickle for metadata storage
- **Performance**: O(n) search, can scale to 1M+ documents

**Embeddings** (`embeddings.py`)
- Sentence Transformers
- Model: all-MiniLM-L6-v2
- Dimension: 384
- **Caching**: Model loaded once, reused

**Ollama Client** (`ollama_client.py`)
- Local LLM integration
- Streaming support (future)
- Fallback responses
- **Timeout**: 120 seconds

### Database Layer

#### SQLAlchemy Models (`app/models/`)

**Tables**:
1. **users**: User accounts
2. **trips**: Trip records
3. **trip_itineraries**: Daily plans
4. **trip_activities**: Individual activities
5. **user_preferences**: User preferences
6. **conversations**: Chat sessions
7. **messages**: Chat messages
8. **knowledge_sources**: Knowledge metadata

**Relationships**:
- User → Trips (one-to-many)
- Trip → Itineraries (one-to-many)
- Itinerary → Activities (one-to-many)
- User → Preferences (one-to-one)
- User → Conversations (one-to-many)
- Conversation → Messages (one-to-many)

---

## Data Flow

### Trip Creation Flow

1. **User Input** → Frontend form/chat
2. **API Request** → POST /api/trips
3. **Workflow Initialization** → LangGraph state
4. **Data Collection**:
   - Parallel API calls to external services
   - Mock data if APIs unavailable
5. **Risk Analysis**:
   - Budget calculation
   - Weather risk scoring
   - Crowding assessment
6. **Knowledge Retrieval**:
   - Query vector store
   - Semantic search
   - Filter and rank
7. **Checkpoint** (if needed):
   - High-risk detected
   - Request user approval
8. **Itinerary Generation**:
   - LLM prompt construction
   - Ollama generation
   - Response parsing
9. **Optimization**:
   - Weather adjustments
   - Budget tweaks
10. **Database Storage**:
    - Save trip record
    - Store itineraries
11. **Response** → Return to frontend

### Chat Flow

1. **User Message** → Frontend
2. **API Request** → POST /api/chat
3. **Conversation Lookup/Create**
4. **Message Storage** → Database
5. **Context Building**:
   - Retrieve message history
   - Add user preferences
6. **LLM Generation** → Ollama
7. **Response Processing**:
   - Parse response
   - Extract suggestions
8. **Message Storage** → Database
9. **Response** → Return to frontend

---

## RAG System Details

### Indexing Pipeline

```
Travel Content (Text)
        ↓
Sentence Transformer
   (Embedding Model)
        ↓
   Embeddings (384D)
        ↓
    FAISS Index
        ↓
Metadata Storage (Pickle)
```

### Retrieval Pipeline

```
User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Top-K Results
    ↓
Metadata Enrichment
    ↓
Filtering & Ranking
    ↓
Sentiment Scoring
    ↓
Final Results
```

### Similarity Calculation

Using L2 distance converted to similarity score:
```python
similarity = exp(-distance)
```

Range: 0 (no similarity) to 1 (identical)

---

## Database Schema

### Entity-Relationship Diagram

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ├──────────────┬───────────────┬─────────────┐
     │              │               │             │
┌────▼────┐    ┌────▼────┐    ┌────▼────┐  ┌────▼────┐
│  Trip   │    │Preference│   │Conversation│ │ ...    │
└────┬────┘    └─────────┘    └────┬────┘  └─────────┘
     │                              │
┌────▼────┐                    ┌────▼────┐
│Itinerary│                    │ Message │
└────┬────┘                    └─────────┘
     │
┌────▼────┐
│Activity │
└─────────┘
```

### Key Indexes

- `users.email`: UNIQUE
- `trips.user_id`: INDEX
- `conversations.user_id`: INDEX
- `messages.conversation_id`: INDEX

---

## Security Considerations

### Current Implementation
- No authentication (demo mode)
- CORS enabled for localhost
- No rate limiting
- SQLite (development database)

### Production Recommendations

1. **Authentication**:
   - JWT tokens
   - OAuth2 integration
   - Refresh tokens

2. **Authorization**:
   - Role-based access control
   - Resource-level permissions

3. **Data Protection**:
   - Encrypt sensitive data
   - HTTPS only
   - API key rotation

4. **Rate Limiting**:
   - Per-IP limits
   - Per-user limits
   - DDoS protection

5. **Input Validation**:
   - Pydantic models
   - SQL injection prevention
   - XSS protection

6. **Database**:
   - PostgreSQL for production
   - Connection pooling
   - Read replicas

7. **Secrets Management**:
   - Environment variables
   - HashiCorp Vault
   - AWS Secrets Manager

---

## Performance Optimization

### Backend
- Async operations for I/O
- Connection pooling
- Caching (Redis for production)
- Background tasks for heavy operations

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- Service workers (PWA)

### RAG System
- FAISS IVF index for large datasets
- Embedding caching
- Batch processing

---

## Monitoring & Observability

### Logging
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request tracing

### Metrics
- Request latency
- Error rates
- Database query performance
- LLM generation time
- Vector search latency

### Health Checks
- `/health` endpoint
- Database connectivity
- Ollama availability
- Vector store status

---

## Scalability

### Horizontal Scaling
- Stateless API design
- Load balancer ready
- Session management (external)

### Vertical Scaling
- Async I/O
- Worker processes (Gunicorn)
- GPU for embeddings/LLM

### Database Scaling
- Read replicas
- Sharding (future)
- Caching layer

---

## Future Enhancements

1. **Real-time Updates**: WebSocket support
2. **Collaborative Planning**: Multi-user trips
3. **Mobile App**: React Native
4. **Booking Integration**: Flights, hotels, activities
5. **Social Features**: Trip sharing, reviews
6. **Advanced ML**: Personalization, recommendations
7. **Multi-language**: i18n support

---

For implementation details, see source code and inline documentation.
