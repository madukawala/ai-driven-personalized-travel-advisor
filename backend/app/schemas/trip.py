from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ActivityResponse(BaseModel):
    """Schema for activity response"""

    id: int
    time_slot: str
    activity_type: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    estimated_cost: Optional[float] = None
    duration_minutes: Optional[int] = None
    booking_required: Optional[str] = None
    tips: Optional[str] = None
    alternatives: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


class ItineraryResponse(BaseModel):
    """Schema for itinerary response"""

    id: int
    day_number: int
    date: datetime
    theme: Optional[str] = None
    description: Optional[str] = None
    weather_forecast: Optional[Dict[str, Any]] = None
    estimated_cost: Optional[float] = None
    activities: List[ActivityResponse] = []

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    """Schema for creating a trip"""

    destination: str = Field(..., description="Destination city/country")
    start_date: datetime = Field(..., description="Trip start date")
    end_date: datetime = Field(..., description="Trip end date")
    budget: float = Field(..., gt=0, description="Trip budget")
    budget_currency: str = Field(default="USD", description="Budget currency")
    interests: List[str] = Field(default=[], description="User interests")
    constraints: Dict[str, Any] = Field(default={}, description="User constraints")


class TripUpdate(BaseModel):
    """Schema for updating a trip"""

    destination: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    budget_currency: Optional[str] = None
    interests: Optional[List[str]] = None
    constraints: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class TripResponse(BaseModel):
    """Schema for trip response"""

    id: int
    user_id: int
    destination: str
    start_date: datetime
    end_date: datetime
    budget: float
    budget_currency: str
    interests: Optional[List[str]] = None
    constraints: Optional[Dict[str, Any]] = None
    status: str
    itinerary_json: Optional[Dict[str, Any]] = None
    risk_analysis: Optional[Dict[str, Any]] = None
    budget_breakdown: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    itineraries: List[ItineraryResponse] = []

    class Config:
        from_attributes = True
