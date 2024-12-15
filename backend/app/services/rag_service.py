from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from ..config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGService:
    """
    Handles RAG (Retrieval Augmented Generation) operations using Pinecone and LangChain.
    This service manages document storage, retrieval, and question answering with 
    customized response generation.
    """
    def __init__(self):
        try:
            logger.info("Initializing RAG Service...")
            
            # Initialize Pinecone and embeddings as before
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.embeddings = OpenAIEmbeddings()
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            
            # Initialize the vector store
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings,
                text_key="text"
            )
            
            # Create our custom prompt template
            self.qa_template = """You are a person named Scott tasked with answering questions based on the provided context, which is content you wrote about yourself and your thoughts. 
            Your goal is to help users understand your point of view as described in the context.

Context Information:
{context}

Question: {question}

Please follow these guidelines when forming your response:
1. Base your answer primarily on the information provided in the context.
2. Explain concepts clearly and thoroughly, breaking down complex ideas when necessary.
3. If the context doesn't contain enough information to fully answer the question, 
acknowledge this and explain what you can based on what's available, but don't refer to "the context" in your response.
Simply say that you don't have enough information to answer the question.
4. Use a tone consistent with the context.
5. Organize your response logically, building from basic concepts to more complex ones.
6. If relevant, provide examples or analogies to illustrate your points.
7. If you quote from the context, integrate it naturally into your explanation.
8. The context provided are your own thoughts and experiences – never refer to it as "the context."

Answer: """

            # Convert the template into a LangChain prompt
            self.QA_PROMPT = PromptTemplate(
                template=self.qa_template,
                input_variables=["context", "question"]
            )
            
            # Set up the QA chain with our custom prompt
            self.qa_chain = self._setup_qa_chain()
            logger.info("RAG Service initialization complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Service: {str(e)}")
            raise

    def _setup_qa_chain(self):
        """
        Creates the retrieval QA chain with the language model and vector store.
        Includes detailed error handling and logging.
        """
        try:
            llm = ChatOpenAI(
                temperature=0.3,
                model_name="gpt-4",
                max_tokens=1000
            )
            # Create the QA chain with custom prompt and verbose logging
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 5}
                ),
                chain_type_kwargs={
                    "prompt": self.QA_PROMPT,
                    "verbose": True 
                }
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