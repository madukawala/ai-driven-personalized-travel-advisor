from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user creation"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""

    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPreferenceCreate(BaseModel):
    """Schema for creating user preferences"""

    favorite_destinations: Optional[List[str]] = None
    preferred_activities: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    accommodation_preferences: Optional[List[str]] = None
    typical_budget_range: Optional[Dict[str, float]] = None
    currency_preference: str = "USD"
    pace: Optional[str] = None
    group_size_preference: Optional[str] = None
    time_constraints: Optional[Dict[str, Any]] = None
    mobility_constraints: Optional[Dict[str, Any]] = None
    eco_conscious: Optional[str] = None
    prefer_public_transit: Optional[str] = None


class UserPreferenceResponse(BaseModel):
    """Schema for user preference response"""

    id: int
    user_id: int
    favorite_destinations: Optional[List[str]] = None
    preferred_activities: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    accommodation_preferences: Optional[List[str]] = None
    typical_budget_range: Optional[Dict[str, float]] = None
    currency_preference: str
    pace: Optional[str] = None
    group_size_preference: Optional[str] = None
    time_constraints: Optional[Dict[str, Any]] = None
    mobility_constraints: Optional[Dict[str, Any]] = None
    eco_conscious: Optional[str] = None
    prefer_public_transit: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
