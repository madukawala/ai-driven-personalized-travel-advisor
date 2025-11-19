from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "AI Travel Advisor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./travel_advisor.db"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"

    # External APIs
    OPENWEATHER_API_KEY: str = ""
    EVENTBRITE_API_KEY: str = ""
    EXCHANGERATE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Vector Store
    FAISS_INDEX_PATH: str = "./data/faiss_index"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # RAG Configuration
    MAX_RETRIEVAL_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.7

    # Agent Configuration
    WEATHER_RISK_THRESHOLD: float = 0.7
    BUDGET_OVERRUN_THRESHOLD: float = 1.2
    DEFAULT_TRIP_DAYS: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
