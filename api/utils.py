# GenAi Wealth Management POC
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

## Loading Documents/Files
# def load_document(file):
#     import os
#     name, extension = os.path.splitext(file)

#     if extension == '.txt':
#         from langchain.document_loaders import TextLoader
#         print(f'Loading .txt file: {file}')
#         loader = TextLoader(file)
#     elif extension == '.json':
#         from langchain.document_loaders import JSONLoader
#         import json
#         print(f'Loading .json file: {file}')
#         loader = JSONLoader(file_path=file, jq_schema='.content', text_content=False)
#     elif extension == '.jsonl':
#         from langchain.document_loaders import JSONLoader
#         import json
#         print(f'Loading .jsonl file: {file}')
#         loader = JSONLoader(file_path=file, jq_schema='.content', text_content=False, json_lines=True)
#     data = loader.load()
#     return data

# Define the metadata extraction function.
# def metadata_func(record: dict, metadata: dict) -> dict:
#     metadata["source"] = record.get("source")
#     metadata["seq_num"] = record.get("seq_num")
#     return metadata

# def load_directory(dir, index_name):
#     import os, json
#     from pathlib import Path
#     from langchain_community.document_loaders import MergedDataLoader, DirectoryLoader, JSONLoader, TextLoader
#     # from langchain_text_splitters import RecursiveJsonSplitter

#     # Load all files in directory
#     loader = DirectoryLoader(dir, use_multithreading=True, recursive=True)
#     loaderArray = []
#     docs = loader.load()

#     for doc in docs:
#         filePath = doc.metadata['source']
#         fileName, fileExt = os.path.splitext(filePath)

#         # Load the documents
#         if fileExt == '.txt':
#             print(f'Loading text file: {filePath}')
#             loader = TextLoader(filePath)
#         elif fileExt == '.json':
#             print(f'Loading JSON file: {filePath}')
#             # splitter = RecursiveJsonSplitter(min_chunk_size=256)
#             loader = JSONLoader(file_path=filePath, jq_schema='.[]|tojson', text_content=False)
#         loaderArray.append(loader)
    
#     all_loaders = MergedDataLoader(loaders=loaderArray)
#     docs = all_loaders.load()
#     print(f'\nLoaded {len(docs)} docs from directory.')
#     return docs

## Chunking Data
# def chunk_data(docs, index_name, chunk_size=750, chunk_overlap=0):
#     from langchain.text_splitter import RecursiveCharacterTextSplitter
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size, 
#         chunk_overlap=chunk_overlap, 
#         add_start_index=True
#     )

#     chunks = text_splitter.split_documents(docs)
#     return chunks

## Embedding and Uploading to Vector Database (Pinecone)
def embed_vector_store(index_name):
    from pinecone import Pinecone, ServerlessSpec, PodSpec
    from langchain_pinecone import PineconeVectorStore
    from langchain_openai import OpenAIEmbeddings

    pc = Pinecone()
    use_serverless = False
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1536)

    # load from existing index. otherwise, create new index & load chunks into new index
    # if index_name in pc.list_indexes().names():
    vector_store = PineconeVectorStore.from_existing_index(index_name, embeddings)
    print(f'{index_name} index already exists')
    return vector_store
    # else:
    #     print(f'Creating {index_name} index... ', end='')
    #     if use_serverless:
    #         spec = ServerlessSpec(cloud='aws', region='us-east-1')
    #     else:
    #         spec = PodSpec(environment='gcp-starter')

    #     pc.create_index(  
    #         name=index_name,
    #         dimension=1536,
    #         metric='cosine',
    #         spec=spec
    #     )

    #     while not pc.describe_index(index_name).status['ready']:  
    #         time.sleep(1)
    #     vector_store = PineconeVectorStore.from_documents(chunks, embeddings, index_name=index_name)
    #     print('Done')
    

## Uploading documents to Pinecone
index_name = 'clientdata'
# # delete_index(index_name)

# # Load the documents
# docs = load_directory("files/client-portfolio", index_name)

# # Split it into chunks
# data_chunks = chunk_data(docs, index_name)

# # Embed and load data chunks into vector store
vector_store = embed_vector_store(index_name)
# print(f'vector__store: {vector_store}\n')

## OpenAI Integration
def ask_and_get_answer(vector_store, q):
    from langchain.chains import RetrievalQA
    from langchain_openai import ChatOpenAI

    # chat completion llm
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

    # RetrievalQA chain
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever(), return_source_documents=True)

    answer = chain.invoke(q)
    return answer

## Wealth Management Summarizer App
def summarize_client_portfolio():
    import regex, json
    client_name = 'Vanessa Mitchell' ## Client personas include Richard Thompson, Samantha Hayes, and Vanessa Mitchell
    email_prompt = f'Generate a 5 sentence summary paragraph of all the email threads between the client, {client_name}, and financial advisor. Also, include a 3 bullet point action item plan based on a follow up to the client information.'
    email_summary = ask_and_get_answer(vector_store, email_prompt)['result']
    return email_summary

# Chatbot App
def chatbot_app():
    import time
    i = 1
    print("\nType 'Quit' or 'Exit' to end session.")

    while True:
        q = input('\nQ:')
        i = i + 1
        if q.lower() in ['quit', 'exit']:
            print('Quitting... bye bye!')
            time.sleep(2)
            break

        answer = ask_and_get_answer(vector_store, q)


def chat_interface(message):
    return ask_and_get_answer(vector_store, message)