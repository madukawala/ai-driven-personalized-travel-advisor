from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.base import Base


class Conversation(Base):
    """Conversation model for storing chat sessions"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)

    # Conversation metadata
    title = Column(String, nullable=True)  # Auto-generated or user-defined title
    status = Column(String, default="active")  # active, completed, archived

    # Conversation context
    context = Column(JSON, nullable=True)  # Store context for the conversation

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, status='{self.status}')>"


class Message(Base):
    """Message model for storing individual messages in a conversation"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    # Message content
    role = Column(String, nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)

    # Message metadata
    message_type = Column(String, default="text")  # text, checkpoint, system_alert
    message_metadata = Column(JSON, nullable=True)  # Additional metadata (e.g., sources, reasoning)

    # Human-in-the-loop checkpoint
    requires_approval = Column(String, nullable=True)  # "yes", "no"
    approval_status = Column(String, nullable=True)  # "pending", "approved", "rejected"
    approval_data = Column(JSON, nullable=True)  # Data related to the approval

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"
