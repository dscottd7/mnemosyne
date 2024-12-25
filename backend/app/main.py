import os
import logging
import sys
from fastapi import FastAPI
from .api.endpoints import router
from pinecone import Pinecone
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Set up logging to capture startup issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Ensure logs go to stdout for Cloud Run to capture them
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI(title="RAG API", version="1.0.0")

# Initialize Pinecone globally with new SDK style
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Include our API router
app.include_router(router, prefix="/api/v1")


# Dynamic CORS configuration based on environment
def get_allowed_origins():
    if settings.is_production:
        return [
            "https://your-frontend-url.run.app",
            # Add any other production URLs
        ]
    return [
        "http://localhost:3000",
        "http://frontend:3000"  # For docker-compose networking
    ]


# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}


# Add startup event to log important information
@app.on_event("startup")
async def startup_event():
    # Log all important configuration details
    port = os.getenv("PORT", "8080")
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting application in {settings.ENVIRONMENT} environment")
    logger.info(f"Running on port {settings.PORT}")
    logger.info(f"Python version: {sys.version}")
    
    # Test Pinecone connection early to catch configuration issues
    try:
        index = pc.Index(settings.PINECONE_INDEX_NAME)
        stats = index.describe_index_stats()
        logger.info(f"Successfully connected to Pinecone index: {settings.PINECONE_INDEX_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to Pinecone: {str(e)}")
        # Don't raise the error - let the app start even if Pinecone isn't available
        # This allows the health endpoint to still work


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")
