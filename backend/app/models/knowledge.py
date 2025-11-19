from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from datetime import datetime
from ..database.base import Base


class KnowledgeSource(Base):
    """Knowledge source model for storing travel knowledge metadata"""
    __tablename__ = "knowledge_sources"

    id = Column(Integer, primary_key=True, index=True)

    # Source information
    source_type = Column(String, nullable=False)  # "blog", "article", "reddit", "guidebook"
    source_name = Column(String, nullable=False)  # e.g., "Lonely Planet", "Nomadic Matt"
    source_url = Column(String, nullable=True)

    # Content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)

    # Location and categorization
    destination = Column(String, nullable=True)  # Primary destination
    locations = Column(JSON, nullable=True)  # List of mentioned locations
    categories = Column(JSON, nullable=True)  # ["food", "culture", "adventure"]

    # Sentiment and quality
    sentiment_score = Column(Float, nullable=True)  # -1 to 1 (negative to positive)
    quality_score = Column(Float, nullable=True)  # 0 to 1 (usefulness rating)
    helpfulness_votes = Column(Integer, default=0)

    # Vector embedding metadata
    embedding_id = Column(String, nullable=True)  # ID in the vector store
    embedding_model = Column(String, nullable=True)

    # Metadata
    published_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Language
    language = Column(String, default="en")

    def __repr__(self):
        return f"<KnowledgeSource(id={self.id}, title='{self.title}', source='{self.source_name}')>"
