"""
GraphQL Schema using Strawberry
"""

import strawberry
from typing import List, Optional
from datetime import datetime


# GraphQL Types
@strawberry.type
class Weather:
    condition: str
    high: float
    low: float
    rain_chance: int


@strawberry.type
class Activity:
    time_slot: str
    description: str
    cost: float


@strawberry.type
class DailyItinerary:
    day_number: int
    date: str
    activities: List[Activity]
    estimated_cost: float
    weather: Optional[Weather] = None
    recommendations: Optional[List[str]] = None


@strawberry.type
class Trip:
    id: int
    destination: str
    start_date: str
    end_date: str
    budget: float
    status: str
    quality_score: Optional[float] = None


@strawberry.type
class Message:
    id: int
    role: str
    content: str
    created_at: str


@strawberry.type
class Conversation:
    id: int
    title: Optional[str]
    status: str
    created_at: str
    message_count: int


# GraphQL Inputs
@strawberry.input
class TripInput:
    destination: str
    start_date: str
    end_date: str
    budget: float
    interests: List[str]
    constraints: Optional[str] = "{}"


@strawberry.input
class ChatInput:
    message: str
    conversation_id: Optional[int] = None


# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def trip(self, trip_id: int) -> Optional[Trip]:
        """Get trip by ID"""
        # In production, this would query the database
        return Trip(
            id=trip_id,
            destination="Tokyo",
            start_date="2024-09-02",
            end_date="2024-09-06",
            budget=700.0,
            status="planning",
            quality_score=85.0,
        )

    @strawberry.field
    async def trips(self, user_id: int = 1) -> List[Trip]:
        """List trips for user"""
        # Mock data - in production, query database
        return [
            Trip(
                id=1,
                destination="Tokyo",
                start_date="2024-09-02",
                end_date="2024-09-06",
                budget=700.0,
                status="planning",
                quality_score=85.0,
            )
        ]

    @strawberry.field
    async def conversations(self, user_id: int = 1) -> List[Conversation]:
        """List conversations for user"""
        return []


# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_trip(self, trip_input: TripInput) -> Trip:
        """Create a new trip"""
        # In production, this would create a trip using the workflow
        return Trip(
            id=1,
            destination=trip_input.destination,
            start_date=trip_input.start_date,
            end_date=trip_input.end_date,
            budget=trip_input.budget,
            status="planning",
        )

    @strawberry.mutation
    async def send_message(self, chat_input: ChatInput) -> Message:
        """Send chat message"""
        return Message(
            id=1,
            role="assistant",
            content="I'd be happy to help plan your trip!",
            created_at=datetime.utcnow().isoformat(),
        )


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
