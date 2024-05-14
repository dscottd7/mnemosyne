import time
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
import os
from langchain.document_loaders import TextLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec, PodSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings


class Langchain_Service:
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
    
    def embed_vector_store(self, chunks, index_name='clientdata'):
        pc = Pinecone()
        use_serverless = False
        embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)

        # load from existing index. otherwise, create new index & load chunks into new index
        if index_name in pc.list_indexes().names():
            vector_store = PineconeVectorStore.from_existing_index(index_name, embeddings)
            addeddocs = vector_store.add_documents(chunks)
            print(f'{index_name} index already exists')
        else:
            print(f'Creating {index_name} index... ', end='')
            if use_serverless:
                spec = ServerlessSpec(cloud='aws', region='us-east-1')
            else:
                spec = PodSpec(environment='gcp-starter')

            pc.create_index(  
                name=index_name,
                dimension=1536,
                metric='cosine',
                spec=spec
            )

            while not pc.describe_index(index_name).status['ready']:  
                time.sleep(1)
            vector_store = PineconeVectorStore.from_documents(chunks, embeddings, index_name=index_name)
            print('Done')
        return vector_store