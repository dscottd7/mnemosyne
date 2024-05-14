from ..services.msearch_service import MSearch_Service
from flask import Blueprint, Response, request, jsonify, current_app, send_from_directory
api_route = Blueprint("api_route", __name__)
from api.utils import chat_interface
from flask import render_template
from ..services.langchain_service import Langchain_Service
import os

langchain_service = Langchain_Service()
msearch_service = MSearch_Service()

@api_route.post("/chat")
def chat():
    message = request.form.get('message')
    response = chat_interface(message)['result']
    return render_template('index.html', response=response, message=message)

# @api_route.post("/upload-documents")
# def upload_documents():
#     #Save file to storage ../../static/files
#     if 'file' not in request.files:
#         print('NO FILE PART')
#         return Response("No file part", status=500, mimetype='application/json')
#     file = request.files['file']
#     if file:
#         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    
#     #load document into document loader 
#     data_to_chunk = langchain_service.load_document(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
#     #chunk data
#     chunks = langchain_service.chunk_data(data_to_chunk)
#     #upload chunked data to vector store
#     langchain_service.embed_vector_store(chunks)
#     return Response("{'a':'b'}", status=201, mimetype='application/json')

@api_route.post("/upload-documents-m")
def upload_documents():
    #Save file to storage ../../static/files
    if 'file' not in request.files:
        print('NO FILE PART')
        return Response("No file part", status=500, mimetype='application/json')
    file = request.files['file']
    if file:
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    
    #load document into document loader 
    data_to_chunk = msearch_service.load_document(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    #chunk data
    chunks = msearch_service.chunk_data(data_to_chunk)
    #upload chunked data to vector store
    msearch_service.embed_vector_store(chunks)
    return Response("{'a':'b'}", status=201, mimetype='application/json')

@api_route.get("/health")
def health_check():
    resp = jsonify(success=True)
    return resp