"""
FastAPI Routes: REST API endpoints for the Travel Advisor
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from datetime import datetime
import logging

from ..database import get_db
from ..models import User, Trip, Conversation, Message, UserPreference
from ..schemas.trip import TripCreate, TripResponse, TripUpdate
from ..schemas.chat import ChatRequest, ChatResponse, ConversationResponse
from ..schemas.user import (
    UserCreate,
    UserResponse,
    UserPreferenceCreate,
    UserPreferenceResponse,
)
from ..agents.langgraph_workflow import TripPlanningWorkflow

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== Trip Endpoints ====================


@router.post("/trips", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip_data: TripCreate,
    user_id: int = 1,  # Simplified - in production, get from auth
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new trip and generate itinerary using LangGraph workflow
    """
    try:
        logger.info(f"Creating trip for destination: {trip_data.destination}")

        # Initialize workflow
        workflow = TripPlanningWorkflow()

        # Prepare initial state
        initial_state = {
            "destination": trip_data.destination,
            "start_date": trip_data.start_date.isoformat(),
            "end_date": trip_data.end_date.isoformat(),
            "budget": trip_data.budget,
            "interests": trip_data.interests,
            "constraints": trip_data.constraints,
            "user_id": user_id,
        }

        # Run workflow
        result = await workflow.run(initial_state)

        # Create trip in database
        trip = Trip(
            user_id=user_id,
            destination=trip_data.destination,
            start_date=trip_data.start_date,
            end_date=trip_data.end_date,
            budget=trip_data.budget,
            budget_currency=trip_data.budget_currency,
            interests=trip_data.interests,
            constraints=trip_data.constraints,
            status="planning",
            itinerary_json=result.get("itinerary", {}),
            risk_analysis=result.get("risk_analysis", {}),
            quality_score=result.get("risk_analysis", {})
            .get("quality_score", {})
            .get("overall_score"),
        )

        db.add(trip)
        await db.commit()
        await db.refresh(trip)

        logger.info(f"Trip created successfully with ID: {trip.id}")

        return {
            "trip_id": trip.id,
            "status": "success",
            "message": result.get("summary_message", "Trip created successfully"),
            "requires_approval": result.get("requires_approval", False),
            "approval_message": result.get("approval_message"),
            "itinerary": result.get("itinerary"),
            "risk_analysis": result.get("risk_analysis"),
            "warnings": result.get("warnings", []),
        }

    except Exception as e:
        logger.error(f"Error creating trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trip: {str(e)}",
        )


@router.get("/trips/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    """Get trip by ID"""
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    return trip


@router.get("/trips", response_model=List[TripResponse])
async def list_trips(
    user_id: int = 1,  # Simplified
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """List trips for a user"""
    result = await db.execute(
        select(Trip)
        .where(Trip.user_id == user_id)
        .order_by(Trip.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    trips = result.scalars().all()
    return trips


@router.put("/trips/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: int, trip_data: TripUpdate, db: AsyncSession = Depends(get_db)
):
    """Update trip"""
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    # Update fields
    for field, value in trip_data.dict(exclude_unset=True).items():
        setattr(trip, field, value)

    await db.commit()
    await db.refresh(trip)

    return trip


@router.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    """Delete trip"""
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    await db.delete(trip)
    await db.commit()


# ==================== Chat Endpoints ====================


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    user_id: int = 1,  # Simplified
    db: AsyncSession = Depends(get_db),
):
    """
    Chat with AI travel advisor
    """
    try:
        # Get or create conversation
        if chat_request.conversation_id:
            result = await db.execute(
                select(Conversation).where(
                    Conversation.id == chat_request.conversation_id
                )
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found",
                )
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                trip_id=chat_request.trip_id,
                title=f"Travel Chat - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                status="active",
            )
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message,
        )
        db.add(user_message)

        # Process message with AI (simplified - in production, use full NLP pipeline)
        from ..rag.ollama_client import OllamaClient

        ollama = OllamaClient()

        # Build context from conversation history
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(10)
        )
        recent_messages = result.scalars().all()

        # Build chat history
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(recent_messages)
        ]
        messages.append({"role": "user", "content": chat_request.message})

        # Generate response
        system_prompt = (
            "You are a helpful travel advisor AI. Help users plan their trips, "
            "provide recommendations, and answer travel-related questions. "
            "Be friendly, informative, and concise."
        )

        ai_response = await ollama.chat(messages, temperature=0.7)

        # Save AI response
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response,
        )
        db.add(ai_message)

        # Update conversation
        conversation.last_message_at = datetime.utcnow()
        await db.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            message=ai_response,
            role="assistant",
            suggestions=["Tell me more", "What else should I know?", "Plan my trip"],
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}",
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    user_id: int = 1, skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):
    """List user conversations"""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.last_message_at.desc())
        .offset(skip)
        .limit(limit)
    )
    conversations = result.scalars().all()

    # Add message count
    response = []
    for conv in conversations:
        result = await db.execute(
            select(Message).where(Message.conversation_id == conv.id)
        )
        message_count = len(result.scalars().all())

        response.append(
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                trip_id=conv.trip_id,
                title=conv.title,
                status=conv.status,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                last_message_at=conv.last_message_at,
                message_count=message_count,
            )
        )

    return response


# ==================== User & Preferences Endpoints ====================


@router.get("/users/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = 1,  # Simplified
    db: AsyncSession = Depends(get_db),
):
    """Get current user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        # Create default user for demo
        user = User(
            email="demo@traveladvisor.com",
            username="demo_user",
            hashed_password="demo",  # Not secure - for demo only
            full_name="Demo User",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


@router.post("/users/preferences", response_model=UserPreferenceResponse)
async def create_or_update_preferences(
    preferences: UserPreferenceCreate,
    user_id: int = 1,
    db: AsyncSession = Depends(get_db),
):
    """Create or update user preferences"""
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        # Update existing
        for field, value in preferences.dict(exclude_unset=True).items():
            setattr(existing, field, value)
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        # Create new
        new_pref = UserPreference(user_id=user_id, **preferences.dict())
        db.add(new_pref)
        await db.commit()
        await db.refresh(new_pref)
        return new_pref


@router.get("/users/preferences", response_model=UserPreferenceResponse)
async def get_preferences(user_id: int = 1, db: AsyncSession = Depends(get_db)):
    """Get user preferences"""
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)
    )
    preferences = result.scalar_one_or_none()

    if not preferences:
        # Return default preferences
        return UserPreferenceResponse(
            id=0,
            user_id=user_id,
            currency_preference="USD",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    return preferences


@router.get("/memory/{user_id}", response_model=Dict[str, Any])
async def get_user_memory(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user's trip history and preferences (memory)"""
    # Get trips
    result = await db.execute(
        select(Trip)
        .where(Trip.user_id == user_id)
        .order_by(Trip.created_at.desc())
        .limit(10)
    )
    trips = result.scalars().all()

    # Get preferences
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)
    )
    preferences = result.scalar_one_or_none()

    return {
        "user_id": user_id,
        "past_trips": [
            {
                "id": trip.id,
                "destination": trip.destination,
                "dates": f"{trip.start_date} to {trip.end_date}",
                "budget": trip.budget,
                "quality_score": trip.quality_score,
            }
            for trip in trips
        ],
        "preferences": preferences.dict() if preferences else {},
        "trip_count": len(trips),
    }
