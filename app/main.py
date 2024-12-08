from fastapi import FastAPI
from .api.endpoints import router
from pinecone import Pinecone  # New import
from .config import settings

# Initialize the FastAPI application
app = FastAPI(title="RAG API", version="1.0.0")

# Initialize Pinecone globally with new SDK style
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Include our API router
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}