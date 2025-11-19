# API Documentation

Complete API reference for the AI-Driven Personalized Travel Advisor.

## Base URL

**Development**: `http://localhost:8000`
**Production**: `https://your-domain.com`

## Authentication

Currently simplified for demo. In production, implement JWT authentication.

## REST API Endpoints

### Health & Info

#### GET /
Get API information

**Response**:
```json
{
  "message": "Welcome to AI Travel Advisor API",
  "version": "1.0.0",
  "status": "online"
}
```

#### GET /health
Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### Trips

#### POST /api/trips
Create a new trip with AI-generated itinerary

**Request Body**:
```json
{
  "destination": "Tokyo",
  "start_date": "2024-09-02T00:00:00",
  "end_date": "2024-09-06T00:00:00",
  "budget": 700.0,
  "budget_currency": "USD",
  "interests": ["food", "culture", "art"],
  "constraints": {
    "no_early_mornings": true,
    "dietary": "vegan"
  }
}
```

**Response** (201 Created):
```json
{
  "trip_id": 1,
  "status": "success",
  "message": "Trip created successfully!",
  "requires_approval": false,
  "approval_message": null,
  "itinerary": {
    "destination": "Tokyo",
    "start_date": "2024-09-02T00:00:00",
    "end_date": "2024-09-06T00:00:00",
    "total_days": 5,
    "budget": 700.0,
    "daily_itineraries": [...]
  },
  "risk_analysis": {...},
  "warnings": []
}
```

#### GET /api/trips
List all trips for user

**Query Parameters**:
- `user_id` (int, optional): User ID (default: 1)
- `skip` (int, optional): Pagination offset (default: 0)
- `limit` (int, optional): Max results (default: 10)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 1,
    "destination": "Tokyo",
    "start_date": "2024-09-02T00:00:00",
    "end_date": "2024-09-06T00:00:00",
    "budget": 700.0,
    "budget_currency": "USD",
    "interests": ["food", "culture"],
    "status": "planning",
    "quality_score": 85.0,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

#### GET /api/trips/{trip_id}
Get trip details by ID

**Response** (200 OK):
```json
{
  "id": 1,
  "destination": "Tokyo",
  "itinerary_json": {...},
  "risk_analysis": {...},
  "quality_score": 85.0
}
```

#### PUT /api/trips/{trip_id}
Update trip

**Request Body**:
```json
{
  "status": "confirmed",
  "budget": 800.0
}
```

#### DELETE /api/trips/{trip_id}
Delete trip (204 No Content)

---

### Chat

#### POST /api/chat
Send chat message to AI advisor

**Request Body**:
```json
{
  "message": "Tell me about food in Tokyo",
  "conversation_id": null,
  "trip_id": null,
  "context": {}
}
```

**Response** (200 OK):
```json
{
  "conversation_id": 1,
  "message": "Tokyo offers incredible food experiences...",
  "role": "assistant",
  "metadata": null,
  "requires_approval": false,
  "sources": [...],
  "suggestions": [
    "Tell me more",
    "What about budget?"
  ]
}
```

#### GET /api/conversations
List conversations

**Query Parameters**:
- `user_id` (int): User ID
- `skip` (int): Offset
- `limit` (int): Max results

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 1,
    "trip_id": null,
    "title": "Travel Chat - 2024-01-15",
    "status": "active",
    "created_at": "2024-01-15T10:00:00",
    "message_count": 12
  }
]
```

---

### Users & Preferences

#### GET /api/users/me
Get current user info

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "demo@traveladvisor.com",
  "username": "demo_user",
  "full_name": "Demo User",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00"
}
```

#### POST /api/users/preferences
Create or update user preferences

**Request Body**:
```json
{
  "favorite_destinations": ["Tokyo", "Paris"],
  "preferred_activities": ["food", "culture"],
  "dietary_restrictions": ["vegan"],
  "typical_budget_range": {"min": 500, "max": 2000},
  "currency_preference": "USD",
  "pace": "moderate",
  "eco_conscious": "yes",
  "prefer_public_transit": "yes"
}
```

#### GET /api/users/preferences
Get user preferences

#### GET /api/memory/{user_id}
Get user's trip history and preferences (memory)

**Response** (200 OK):
```json
{
  "user_id": 1,
  "past_trips": [...],
  "preferences": {...},
  "trip_count": 5
}
```

---

## GraphQL API

### Endpoint
`POST /graphql` or visit `/graphql` for playground

### Queries

#### Get Trip
```graphql
query {
  trip(trip_id: 1) {
    id
    destination
    start_date
    end_date
    budget
    status
    quality_score
  }
}
```

#### List Trips
```graphql
query {
  trips(user_id: 1) {
    id
    destination
    start_date
    end_date
    budget
    status
  }
}
```

#### List Conversations
```graphql
query {
  conversations(user_id: 1) {
    id
    title
    status
    message_count
  }
}
```

### Mutations

#### Create Trip
```graphql
mutation {
  createTrip(tripInput: {
    destination: "Tokyo"
    start_date: "2024-09-02"
    end_date: "2024-09-06"
    budget: 700.0
    interests: ["food", "culture"]
  }) {
    id
    destination
    status
  }
}
```

#### Send Message
```graphql
mutation {
  sendMessage(chatInput: {
    message: "Plan a trip to Paris"
    conversation_id: null
  }) {
    id
    role
    content
    created_at
  }
}
```

---

## Data Schemas

### Trip Schema
```python
{
  "id": int,
  "user_id": int,
  "destination": string,
  "start_date": datetime,
  "end_date": datetime,
  "budget": float,
  "budget_currency": string,
  "interests": list[string],
  "constraints": dict,
  "status": string,  # "planning", "confirmed", "completed", "cancelled"
  "itinerary_json": dict,
  "risk_analysis": dict,
  "quality_score": float,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Itinerary Schema
```python
{
  "destination": string,
  "start_date": string,
  "end_date": string,
  "total_days": int,
  "budget": float,
  "daily_itineraries": [
    {
      "day_number": int,
      "date": string,
      "theme": string,
      "weather": {...},
      "activities": [
        {
          "time_slot": string,
          "activity_type": string,
          "title": string,
          "description": string,
          "location": string,
          "estimated_cost": float,
          "tips": string
        }
      ],
      "estimated_cost": float,
      "recommendations": list[string]
    }
  ],
  "summary": {
    "total_estimated_cost": float,
    "average_daily_cost": float
  }
}
```

### Risk Analysis Schema
```python
{
  "budget_risk": {
    "estimated_cost": float,
    "budget": float,
    "overrun_risk": string,  # "low", "medium", "high"
    "overrun_percentage": int,
    "recommendations": list[string]
  },
  "weather_risk": {
    "risk_level": string,
    "rainy_days": int,
    "total_days": int,
    "rain_percentage": float,
    "recommendations": list[string]
  },
  "crowding_risk": {
    "risk_level": string,
    "major_events": list[dict],
    "holidays": list[dict],
    "recommendations": list[string]
  },
  "quality_score": {
    "overall_score": float,
    "comfort_level": string,
    "component_scores": {
      "budget": float,
      "weather": float,
      "crowding": float
    }
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Trip not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Error message"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. For production:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## WebSocket Support

Future feature for real-time updates during trip planning.

---

## Testing with cURL

### Create Trip
```bash
curl -X POST http://localhost:8000/api/trips \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "start_date": "2024-09-02T00:00:00",
    "end_date": "2024-09-06T00:00:00",
    "budget": 700.0,
    "interests": ["food", "culture"]
  }'
```

### List Trips
```bash
curl http://localhost:8000/api/trips?user_id=1
```

### Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Plan a trip to Paris"
  }'
```

---

## SDKs & Client Libraries

Coming soon:
- Python client library
- JavaScript/TypeScript SDK
- React hooks library

---

For more details, visit the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **GraphQL Playground**: `http://localhost:8000/graphql`
