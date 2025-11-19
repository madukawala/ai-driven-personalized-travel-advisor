"""
Test cases for database models
Run with: pytest tests/test_models.py -v
"""

import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.models.trip import Trip
from app.models.conversation import Conversation, Message
from app.models.preference import UserPreference
# Note: UserMemory model may not exist - tests will be skipped


def test_user_model_creation():
    """Test User model creation"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword123"
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpassword123"
    assert user.is_active is True
    assert user.created_at is not None


def test_user_model_relationships():
    """Test User model has relationship attributes"""
    user = User(username="test", email="test@example.com", hashed_password="hash")

    # Check that relationship attributes exist
    assert hasattr(user, 'trips')
    assert hasattr(user, 'conversations')
    assert hasattr(user, 'preferences')


def test_trip_model_creation():
    """Test Trip model creation"""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=5)

    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=start_date,
        end_date=end_date,
        budget=800.0,
        interests=["food", "culture"]
    )

    assert trip.destination == "Tokyo"
    assert trip.budget == 800.0
    assert isinstance(trip.interests, list)
    assert len(trip.interests) == 2
    assert trip.created_at is not None


def test_trip_model_with_itinerary():
    """Test Trip model with itinerary"""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=5)

    itinerary = {
        "daily_itineraries": [
            {"day": 1, "activities": ["Visit temple", "Try sushi"]}
        ],
        "summary": {"total_cost": 750}
    }

    trip = Trip(
        user_id=1,
        destination="Kyoto",
        start_date=start_date,
        end_date=end_date,
        budget=1000.0,
        interests=["culture"],
        itinerary=itinerary
    )

    assert trip.itinerary is not None
    assert "daily_itineraries" in trip.itinerary
    assert "summary" in trip.itinerary


def test_trip_model_with_quality_score():
    """Test Trip model with quality score"""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3)

    trip = Trip(
        user_id=1,
        destination="Osaka",
        start_date=start_date,
        end_date=end_date,
        budget=600.0,
        interests=["food"],
        quality_score=85
    )

    assert trip.quality_score == 85
    assert 0 <= trip.quality_score <= 100


def test_trip_model_with_constraints():
    """Test Trip model with constraints"""
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)

    constraints = {
        "dietary_restrictions": ["vegetarian"],
        "accommodation_type": "hotel",
        "mobility_requirements": None
    }

    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=start_date,
        end_date=end_date,
        budget=800.0,
        interests=["food"],
        constraints=constraints
    )

    assert trip.constraints is not None
    assert "dietary_restrictions" in trip.constraints
    assert trip.constraints["dietary_restrictions"] == ["vegetarian"]


def test_conversation_model_creation():
    """Test Conversation model creation"""
    conv = Conversation(
        user_id=1,
        title="Trip to Tokyo"
    )

    assert conv.user_id == 1
    assert conv.title == "Trip to Tokyo"
    assert conv.created_at is not None
    assert conv.updated_at is not None


def test_conversation_model_relationships():
    """Test Conversation has messages relationship"""
    conv = Conversation(user_id=1, title="Test")

    assert hasattr(conv, 'messages')


def test_message_model_creation():
    """Test Message model creation"""
    message = Message(
        conversation_id=1,
        role="user",
        content="I want to visit Tokyo"
    )

    assert message.conversation_id == 1
    assert message.role == "user"
    assert message.content == "I want to visit Tokyo"
    assert message.created_at is not None


def test_message_model_roles():
    """Test Message model with different roles"""
    user_msg = Message(
        conversation_id=1,
        role="user",
        content="Hello"
    )

    assistant_msg = Message(
        conversation_id=1,
        role="assistant",
        content="Hi! How can I help?"
    )

    assert user_msg.role == "user"
    assert assistant_msg.role == "assistant"


def test_user_preference_model_creation():
    """Test UserPreference model creation"""
    pref = UserPreference(
        user_id=1,
        dietary_restrictions=["vegetarian", "gluten-free"],
        accommodation_type="hotel",
        transportation_preference="public",
        interests=["food", "culture", "nature"]
    )

    assert pref.user_id == 1
    assert isinstance(pref.dietary_restrictions, list)
    assert "vegetarian" in pref.dietary_restrictions
    assert pref.accommodation_type == "hotel"
    assert pref.transportation_preference == "public"


def test_user_preference_model_optional_fields():
    """Test UserPreference with optional fields"""
    pref = UserPreference(
        user_id=1,
        dietary_restrictions=None,
        accommodation_type="hostel"
    )

    assert pref.dietary_restrictions is None or pref.dietary_restrictions == []
    assert pref.accommodation_type == "hostel"


@pytest.mark.skip(reason="UserMemory model not implemented yet")
def test_user_memory_model_creation():
    """Test UserMemory model creation"""
    # Placeholder test - UserMemory model may be added later
    pass


@pytest.mark.skip(reason="UserMemory model not implemented yet")
def test_user_memory_model_feedback():
    """Test UserMemory with feedback"""
    # Placeholder test - UserMemory model may be added later
    pass


def test_trip_duration_calculation():
    """Test trip duration calculation"""
    start_date = datetime(2024, 9, 1)
    end_date = datetime(2024, 9, 6)

    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=start_date,
        end_date=end_date,
        budget=1000.0,
        interests=["food"]
    )

    duration = (trip.end_date - trip.start_date).days
    assert duration == 5


def test_trip_with_empty_interests():
    """Test Trip with empty interests list"""
    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=3),
        budget=500.0,
        interests=[]
    )

    assert isinstance(trip.interests, list)
    assert len(trip.interests) == 0


def test_conversation_with_no_title():
    """Test Conversation without explicit title"""
    conv = Conversation(user_id=1)

    # Should have default or None
    assert conv.user_id == 1


def test_model_timestamps():
    """Test that models have proper timestamps"""
    user = User(username="test", email="test@example.com", hashed_password="hash")
    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=3),
        budget=800.0,
        interests=["food"]
    )
    conv = Conversation(user_id=1, title="Test")

    # All should have created_at
    assert hasattr(user, 'created_at')
    assert hasattr(trip, 'created_at')
    assert hasattr(conv, 'created_at')


def test_trip_model_status():
    """Test Trip model status field"""
    trip = Trip(
        user_id=1,
        destination="Tokyo",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=3),
        budget=800.0,
        interests=["food"],
        status="planned"
    )

    assert trip.status == "planned"


def test_user_preference_pace():
    """Test UserPreference pace preference"""
    pref = UserPreference(
        user_id=1,
        pace_preference="relaxed"
    )

    assert pref.pace_preference == "relaxed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
