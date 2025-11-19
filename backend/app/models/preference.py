from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base


class UserPreference(Base):
    """User preference model for storing learned preferences"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Travel preferences
    favorite_destinations = Column(JSON, nullable=True)  # List of favorite destinations
    preferred_activities = Column(JSON, nullable=True)  # List of activity types
    dietary_restrictions = Column(JSON, nullable=True)  # e.g., ["vegan", "gluten-free"]
    accommodation_preferences = Column(JSON, nullable=True)  # e.g., ["hotel", "hostel", "airbnb"]

    # Budget preferences
    typical_budget_range = Column(JSON, nullable=True)  # {"min": 500, "max": 2000}
    currency_preference = Column(String, default="USD")

    # Travel style
    pace = Column(String, nullable=True)  # "relaxed", "moderate", "packed"
    group_size_preference = Column(String, nullable=True)  # "solo", "couple", "family", "group"

    # Constraints
    time_constraints = Column(JSON, nullable=True)  # e.g., {"no_early_mornings": true, "prefer_afternoon": true}
    mobility_constraints = Column(JSON, nullable=True)  # Any mobility limitations

    # Eco preferences (for eco-aware planning)
    eco_conscious = Column(String, nullable=True)  # "yes", "no", "moderate"
    prefer_public_transit = Column(String, nullable=True)  # "yes", "no", "when_convenient"

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id})>"
