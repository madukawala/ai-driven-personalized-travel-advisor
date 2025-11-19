"""
FastAPI Main Application
AI-Driven Personalized Travel Advisor
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from .utils.config import settings
from .database import init_db
from .api import routes

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for FastAPI app"""
    # Startup
    logger.info("Starting AI Travel Advisor API...")

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    # Initialize vector store (will load existing if available)
    try:
        from .rag.vector_store import VectorStore

        vector_store = VectorStore()
        logger.info(
            f"Vector store initialized with {vector_store.get_document_count()} documents"
        )
    except Exception as e:
        logger.error(f"Vector store initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down AI Travel Advisor API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Driven Personalized Travel Advisor API with RAG and LangGraph",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Travel Advisor API",
        "version": settings.APP_VERSION,
        "status": "online",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
    }


# Include REST API routes
app.include_router(routes.router, prefix="/api")

# Include GraphQL endpoint (if available - disabled on Python 3.14)
try:
    import strawberry
    from strawberry.fastapi import GraphQLRouter
    from .api.graphql_schema import schema

    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    logger.info("GraphQL endpoint enabled at /graphql")
except (ImportError, Exception) as e:
    logger.warning(f"GraphQL endpoint disabled (Python 3.14 compatibility): {e}")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
