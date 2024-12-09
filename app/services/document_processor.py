from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, BinaryIO
import pypdf
import logging
import tempfile
import os

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Handles the processing of simple PDF documents for RAG system. 
    This processor focuses on clean text extraction and 
    intelligent chunking to maintain the natural flow of the documents.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # We use RecursiveCharacterTextSplitter because it respects natural text 
        # boundaries like paragraphs and sentences, which is perfect for Word-based PDFs
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            # These separators help maintain the document's natural structure
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        logger.info(f"Initialized PDF processor with {chunk_size} character chunks")

    def process_pdf(self, pdf_file: BinaryIO) -> List[str]:
        """
        Extracts and chunks text from a PDF file. This method is optimized for
        PDFs that were created from Word documents, ensuring we preserve the
        natural flow and structure of the original text.
        """
        try:
            # Save the uploaded file temporarily so PyPDF can access it
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_file.read())
                tmp_path = tmp_file.name

            # Extract text from the PDF
            reader = pypdf.PdfReader(tmp_path)
            
            # Combine text from all pages, maintaining paragraph breaks
            text_content = []
            for page in reader.pages:
                # extract_text() works well for PDFs created from Word
                page_text = page.extract_text()
                # Preserve paragraph breaks that might be in the original
                text_content.append(page_text.strip())
            
            # Join pages with double newlines to maintain paragraph separation
            full_text = "\n\n".join(text_content)
            
            # Split the text into chunks that respect natural boundaries
            chunks = self.text_splitter.split_text(full_text)
            
            # Clean up our temporary file
            os.unlink(tmp_path)
            
            logger.info(f"Successfully processed PDF into {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
