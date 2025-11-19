from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base


class Trip(Base):
    """Trip model for storing trip information"""
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget = Column(Float, nullable=False)
    budget_currency = Column(String, default="USD")

    # Trip preferences
    interests = Column(JSON, nullable=True)  # List of interests (e.g., ["food", "art", "history"])
    constraints = Column(JSON, nullable=True)  # User constraints (e.g., {"no_early_mornings": true})

    # Trip status
    status = Column(String, default="planning")  # planning, confirmed, completed, cancelled

    # Generated itinerary and analysis
    itinerary_json = Column(JSON, nullable=True)
    risk_analysis = Column(JSON, nullable=True)
    budget_breakdown = Column(JSON, nullable=True)
    quality_score = Column(Float, nullable=True)  # Overall trip quality score (0-100)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="trips")
    itineraries = relationship("TripItinerary", back_populates="trip", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trip(id={self.id}, destination='{self.destination}', status='{self.status}')>"


class TripItinerary(Base):
    """Daily itinerary for a trip"""
    __tablename__ = "trip_itineraries"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    # Day summary
    theme = Column(String, nullable=True)  # e.g., "Cultural Exploration", "Food Adventure"
    description = Column(Text, nullable=True)

    # Weather and conditions
    weather_forecast = Column(JSON, nullable=True)

    # Activities for the day
    activities_json = Column(JSON, nullable=True)

    # Daily budget
    estimated_cost = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="itineraries")
    activities = relationship("TripActivity", back_populates="itinerary", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TripItinerary(id={self.id}, trip_id={self.trip_id}, day={self.day_number})>"


class TripActivity(Base):
    """Individual activity in an itinerary"""
    __tablename__ = "trip_activities"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("trip_itineraries.id"), nullable=False)

    # Activity details
    time_slot = Column(String, nullable=False)  # e.g., "09:00-12:00"
    activity_type = Column(String, nullable=False)  # e.g., "sightseeing", "dining", "transport"
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)

    # Cost and logistics
    estimated_cost = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    booking_required = Column(String, nullable=True)  # "yes", "recommended", "no"

    # Recommendations
    tips = Column(Text, nullable=True)
    alternatives = Column(JSON, nullable=True)  # Alternative suggestions

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    itinerary = relationship("TripItinerary", back_populates="activities")

    def __repr__(self):
        return f"<TripActivity(id={self.id}, title='{self.title}', time='{self.time_slot}')>"
