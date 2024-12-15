from fastapi import FastAPI
from .api.endpoints import router
from pinecone import Pinecone
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(title="RAG API", version="1.0.0")

# Initialize Pinecone globally with new SDK style
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Include our API router
app.include_router(router, prefix="/api/v1")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}