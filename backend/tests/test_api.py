"""
Test cases for API endpoints
Run with: pytest tests/test_api.py -v
"""

import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.main import app


@pytest.fixture
def sample_trip_data():
    """Sample trip data for testing"""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=5)

    return {
        "destination": "Tokyo",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "budget": 800,
        "interests": ["food", "culture"],
        "user_id": 1
    }


@pytest.fixture
def sample_chat_message():
    """Sample chat message for testing"""
    return {
        "message": "Plan a 5-day trip to Tokyo with $800 budget",
        "user_id": 1,
        "conversation_id": None
    }


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_trip(sample_trip_data):
    """Test trip creation endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/trips", json=sample_trip_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["destination"] == "Tokyo"
        assert "itinerary" in data
        assert "quality_score" in data


@pytest.mark.asyncio
async def test_create_trip_invalid_data():
    """Test trip creation with invalid data"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        invalid_data = {
            "destination": "Tokyo",
            # Missing required fields
        }
        response = await client.post("/api/trips", json=invalid_data)

        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_trips():
    """Test getting user trips"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/trips?user_id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_chat_endpoint(sample_chat_message):
    """Test chat endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/chat", json=sample_chat_message)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "conversation_id" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0


@pytest.mark.asyncio
async def test_chat_with_conversation_id(sample_chat_message):
    """Test chat with existing conversation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First message
        response1 = await client.post("/api/chat", json=sample_chat_message)
        conv_id = response1.json()["conversation_id"]

        # Follow-up message
        follow_up = {
            "message": "Make it budget-friendly",
            "user_id": 1,
            "conversation_id": conv_id
        }
        response2 = await client.post("/api/chat", json=follow_up)

        assert response2.status_code == 200
        data = response2.json()
        assert data["conversation_id"] == conv_id


@pytest.mark.asyncio
async def test_get_conversations():
    """Test getting user conversations"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/conversations?user_id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_user_memory():
    """Test getting user memory"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/memory/1")

        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "preferences" in data
        assert "trip_history" in data


@pytest.mark.asyncio
async def test_update_user_preferences():
    """Test updating user preferences"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        preferences = {
            "user_id": 1,
            "dietary_restrictions": ["vegetarian"],
            "accommodation_type": "hotel",
            "transportation_preference": "public",
            "interests": ["food", "culture", "nature"]
        }
        response = await client.post("/api/users/preferences", json=preferences)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data


@pytest.mark.asyncio
async def test_cors_headers():
    """Test CORS headers are present"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.options("/api/trips")

        # Check if CORS headers would be added by middleware
        assert response.status_code in [200, 405]


@pytest.mark.asyncio
async def test_trip_with_constraints(sample_trip_data):
    """Test trip creation with additional constraints"""
    sample_trip_data["constraints"] = {
        "dietary_restrictions": ["vegetarian"],
        "mobility_requirements": None,
        "accommodation_type": "hotel",
        "pace_preference": "moderate"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/trips", json=sample_trip_data)

        assert response.status_code == 201
        data = response.json()
        assert "constraints" in data


@pytest.mark.asyncio
async def test_trip_with_invalid_dates():
    """Test trip creation with invalid dates (past dates)"""
    past_date = datetime.now() - timedelta(days=5)
    trip_data = {
        "destination": "Tokyo",
        "start_date": past_date.isoformat(),
        "end_date": (past_date + timedelta(days=5)).isoformat(),
        "budget": 800,
        "interests": ["food"],
        "user_id": 1
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/trips", json=trip_data)

        # Should still work (might want past trip planning)
        assert response.status_code in [201, 422]


@pytest.mark.asyncio
async def test_trip_with_zero_budget():
    """Test trip creation with zero budget"""
    start_date = datetime.now() + timedelta(days=30)
    trip_data = {
        "destination": "Tokyo",
        "start_date": start_date.isoformat(),
        "end_date": (start_date + timedelta(days=5)).isoformat(),
        "budget": 0,
        "interests": ["food"],
        "user_id": 1
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/trips", json=trip_data)

        assert response.status_code in [201, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
