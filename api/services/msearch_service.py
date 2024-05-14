import os
from langchain_community.vectorstores import Meilisearch
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class MSearch_Service:
    def load_document(self, file):
        print(file)
        name, extension = os.path.splitext(file)
        print(extension)

        if extension == '.txt':
            print(f'Loading .txt file: {file}')
            loader = TextLoader(file)
        elif extension == '.json':
            print(f'Loading .json file: {file}')
            loader = JSONLoader(file_path=file, jq_schema='.content', text_content=False)
        elif extension == '.jsonl':
            print(f'Loading .jsonl file: {file}')
            loader = JSONLoader(file_path=file, jq_schema='.content', text_content=False, json_lines=True)
        data = loader.load()
        return data

    def chunk_data(self, docs, chunk_size=750, chunk_overlap=0):
        print(docs)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            add_start_index=True
        )

        chunks = text_splitter.split_documents(docs)
        return chunks

    def embed_vector_store(self, chunks):
        embeddings = OpenAIEmbeddings()
        embedders = {
            "default": {
                "source": "userProvided",
                "dimensions": 1536,
            }
        }
        embedder_name = "default"

        vector_store = Meilisearch.from_documents(
        documents=chunks,
        embedding=embeddings,
        embedders=embedders,
        embedder_name=embedder_name,
        )

        query = "What is under the sea?"
        docs = vector_store.similarity_search(query, embedder_name=embedder_name)
        print(docs[0].page_content)