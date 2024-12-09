from fastapi import APIRouter, HTTPException, UploadFile, File
import io
from pydantic import BaseModel
from typing import List
from ..services.rag_service import RAGService
from ..services.document_processor import DocumentProcessor
import logging

document_processor = DocumentProcessor()
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


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Process a PDF file (converted from Word) and add its content to our RAG system.
    The endpoint extracts text, splits it into meaningful chunks, and stores it
    for future retrieval.
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Please upload a PDF file"
            )

        # Read and process the PDF
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)
        text_chunks = document_processor.process_pdf(pdf_file)
        
        # Add the processed chunks to our RAG system
        await rag_service.add_documents(text_chunks)
        
        return {
            "status": "success",
            "message": f"Added {len(text_chunks)} text segments to the knowledge base",
            "number_of_chunks": len(text_chunks)
        }

    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
