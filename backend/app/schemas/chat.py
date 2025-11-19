from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """Schema for a single chat message"""

    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    requires_approval: Optional[bool] = Field(default=False, description="Whether message requires approval")
    approval_data: Optional[Dict[str, Any]] = Field(default=None, description="Approval data")


class ChatRequest(BaseModel):
    """Schema for chat request"""

    message: str = Field(..., description="User message")
    conversation_id: Optional[int] = Field(default=None, description="Conversation ID for continuing chat")
    trip_id: Optional[int] = Field(default=None, description="Trip ID if related to specific trip")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class ChatResponse(BaseModel):
    """Schema for chat response"""

    conversation_id: int
    message: str
    role: str = "assistant"
    metadata: Optional[Dict[str, Any]] = None
    requires_approval: bool = False
    approval_data: Optional[Dict[str, Any]] = None
    sources: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[str]] = None
    trip_data: Optional[Dict[str, Any]] = None


class ConversationResponse(BaseModel):
    """Schema for conversation response"""

    id: int
    user_id: int
    trip_id: Optional[int] = None
    title: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True
