from pinecone import init, Index
from dotenv import dotenv_values
from pprint import pprint
from langchain.vectorstores import Pinecone
import pinecone
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
import os
from ..utils import get_cache, embedding_function

config = {**dotenv_values(".env"), **os.environ}

PINECONE_ENVIRONMENT = config.get("PINECONE_ENVIRONMENT", None)
PINECONE_API_KEY = config.get("PINECONE_API_KEY", None)
PINECONE_INDEX_NAME = config.get("PINECONE_INDEX_NAME", None)


def init_pinecone():
    try:
        if PINECONE_ENVIRONMENT is None or PINECONE_API_KEY is None:
            raise Exception("Pinecone environment or api key vars missing")

        init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    except:
        pprint("error")
        raise Exception("Failed to initialize Pinecone Client")


def create_retriever():
    if PINECONE_INDEX_NAME is None:
        pprint("missing pinecone info")
        raise Exception("PINECONE_INDEX_NAME missing")

    index = Index(index_name=PINECONE_INDEX_NAME)
    embeddings = embedding_function()

    vectorstore = Pinecone(
        index=index,
        embedding=embeddings,
        text_key="text",
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    return retriever


def get_retriever():
    cache = get_cache()
    key = "docs_retriever"
    if key not in cache:
        cache[key] = create_retriever()
    return cache[key]


def upload_documents(directory_path):
    loader = PyPDFDirectoryLoader(directory_path)
    docs = loader.load_and_split()
    embeddings = embedding_function()

    for i in docs:
        if i.metadata.get("page") is None:
            i.metadata["page"] = 1
        else:
            i.metadata["page"] += 1

    # Create and configure index if doesn't already exist
    if PINECONE_INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(name=PINECONE_INDEX_NAME, metric="cosine", dimension=1536)
        docsearch = Pinecone.from_documents(
            documents=docs,
            embeddings=embeddings,
            index_name=PINECONE_INDEX_NAME,
        )
    else:
        docsearch = Pinecone.from_existing_index(
            index_name=PINECONE_INDEX_NAME, embedding=embeddings
        )
        pprint(f"{len(docs)} documents to add")
        vector_ids = docsearch.add_documents(docs)
        pprint(f"{len(vector_ids)} vectors created: {vector_ids}")
