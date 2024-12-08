from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.rag_service import RAGService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class Query(BaseModel):
    question: str


class Documents(BaseModel):
    texts: List[str]


class Answer(BaseModel):
    answer: str


# Initialize the RAG service
try:
    rag_service = RAGService()
except Exception as e:
    logger.error(f"Failed to initialize RAG service: {str(e)}")
    raise


@router.post("/query", response_model=Answer)
async def query_documents(query: Query):
    """
    Endpoint to query documents using RAG.
    """
    try:
        answer = await rag_service.get_answer(query.question)
        return Answer(answer=answer)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents")
async def add_documents(documents: Documents):
    """
    Endpoint to add new documents to the vector store.
    """
    try:
        success = await rag_service.add_documents(documents.texts)
        return {"status": "success", "message": f"Added {len(documents.texts)} documents"}
    except Exception as e:
        logger.error(f"Error adding documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))