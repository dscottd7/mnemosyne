from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from ..config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGService:
    """
    Handles RAG (Retrieval Augmented Generation) operations using Pinecone and LangChain.
    This service manages document storage, retrieval, and question answering.
    """
    def __init__(self):
        try:
            logger.info("Initializing RAG Service...")
            
            # Create Pinecone instance
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            logger.info("Pinecone client initialized")
            
            # Initialize the embeddings model
            self.embeddings = OpenAIEmbeddings()
            logger.info("OpenAI embeddings initialized")
            
            # Get the index - no need to create it as it should already exist
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            logger.info(f"Connected to Pinecone index: {settings.PINECONE_INDEX_NAME}")
            
            # Set up the LangChain vector store
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings,
                text_key="text"
            )
            logger.info("LangChain vector store initialized")
            
            # Initialize the QA chain with error handling
            self.qa_chain = self._setup_qa_chain()
            logger.info("QA chain setup completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Service: {str(e)}")
            # Re-raise the exception to prevent the service from starting in a bad state
            raise

    def _setup_qa_chain(self):
        """
        Creates the retrieval QA chain with the language model and vector store.
        Includes detailed error handling and logging.
        """
        try:
            llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4"
            )
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                )
            )
        except Exception as e:
            logger.error(f"Failed to set up QA chain: {str(e)}")
            raise

    async def get_answer(self, question: str) -> str:
        """
        Processes a question through the RAG pipeline to generate an answer.
        
        Args:
            question: The user's question to be answered
            
        Returns:
            A string containing the generated answer based on retrieved context
        """
        try:
            logger.info(f"Processing question: {question}")
            response = self.qa_chain.invoke(question)
            logger.info("Successfully generated answer")
            return response["result"]
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    async def add_documents(self, texts: list[str]) -> bool:
        """
        Adds new documents to the vector store for future retrieval.
        
        Args:
            texts: List of text documents to be added to the vector store
            
        Returns:
            True if documents were successfully added
        """
        try:
            logger.info(f"Adding {len(texts)} documents to vector store")
            self.vectorstore.add_texts(texts)
            logger.info("Successfully added documents to vector store")
            return True
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise