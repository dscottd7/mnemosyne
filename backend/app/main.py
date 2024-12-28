import logging
import sys
from fastapi import FastAPI
from .api.endpoints import router
from pinecone import Pinecone
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Set up logging with a consistent format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI(title="RAG API", version="1.0.0")

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)


# Define CORS configuration based on environment
def get_allowed_origins():
    """
    Returns appropriate CORS origins based on environment.
    Production uses HTTPS, development uses HTTP.
    """
    if settings.is_production:
        return [
            "https://mnemosyne-frontend-302656282665.us-central1.run.app",
        ]
    return [
        "http://localhost:3000",
        "http://frontend:3000",  # For local docker-compose
    ]


# Configure CORS middleware with environment-specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Length"],
    max_age=600,
)

# Include API router with versioned prefix
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint to verify service status."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler that verifies configurations and connections.
    Logs important setup information and tests critical services.
    """
    logger.info(f"Starting application in {settings.ENVIRONMENT} environment")
    logger.info(f"Running on port {settings.PORT}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"CORS origins: {get_allowed_origins()}")
    
    # Test Pinecone connection
    try:
        index = pc.Index(settings.PINECONE_INDEX_NAME)
        index.describe_index_stats()
        logger.info(f"Successfully connected to Pinecone index: {settings.PINECONE_INDEX_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to Pinecone: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup handler for application shutdown."""
    logger.info("Application shutting down")
