from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from text_processor_crew.src.text_processor_crew.crew import TextProcessorCrew
from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.core import ServiceContext
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import Settings
from llama_index.core import Document
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.llms import ChatMessage, MessageRole
from uuid import uuid4
import os
import re
import chromadb

app = FastAPI()
embed_model = None

# Configure CORS to allow requests from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://bimciljmockmmenihkjongkbpnmomphl"],  # Replace with your extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the text data
class TextData(BaseModel):
    content: str

@app.post("/process-text/")
async def process_text(data: TextData):
    # print("Received text:", data.content)  # For debugging
    print("process_text called")
    uncleaned_text = data.content
    get_nims_embeddings(uncleaned_text)
    return {"message": "Text received successfully.", "content_length": len(data.content)}

@app.post("/process-query/")
async def process_query(data: TextData):
    # print("Received user query:", data.content)  # For debugging
    user_query = data.content
    response_message = f"Processed query: {user_query}"
    context = retrieve_query_related_embeddings(user_query)
    print(context)
    generate_response(context, user_query)
    return {"message": response_message}

def generate_response(context, user_query):
    # Initialize the NVIDIA LLM
    llm = NVIDIA(model='nvidia/llama-3.1-nemotron-70b-instruct')

    # Set the LLM in global settings
    Settings.llm = llm

    # Prepare the prompt by combining context and user query
    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM, content=("You are a helpful assistant and use the context provided in this message to answer users query. " + str(context))
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(user_query),
        ),
    ]

    # prompt = [f"Context: {context}\n\nUser Query: {user_query}\n\nGenerate a helpful response based on the context provided."]
    # print(prompt)
    # Generate a response using the LLM
    response = llm.chat(messages)
    print(response)
    # print(response.response_text)
    return response

def clean_text(text):
    text = re.sub(r'(\b\w+\b)(\s+\1)+', r'\1', text)
    text = re.sub(r'\bundefined\b', '', text)  # Remove "undefined" instances
    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip() and not re.match(r'^[\W_]+$', line)]
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text.strip()

def get_nims_embeddings(uncleaned_text):
    global embed_model
    embed_model = NVIDIAEmbedding(model="nvidia/nv-embedqa-mistral-7b-v2")
    splitter = TokenTextSplitter(chunk_size=256, chunk_overlap=10, backup_separators=["\n"], include_prev_next_rel=True)

    cleaned_text = clean_text(uncleaned_text)
    chunks = splitter.split_text(cleaned_text)
    print(len(chunks), len(chunks[0]))

    embeddings = embed_model.get_text_embedding_batch(chunks)
    print(len(embeddings))
    client, collection = create_vectorb()
    add_to_chroma(chunks, embeddings, client, collection)

def retrieve_query_related_embeddings(user_query):
    global embed_model
    client = chromadb.PersistentClient(path="RAGE_DB")
    collection_name = "RAGE-DB"
    collection = client.get_or_create_collection(name=collection_name)
    user_query_embeddings = embed_model.get_text_embedding(user_query)
    results = collection.query(query_embeddings=user_query_embeddings, n_results=5)
    return results['documents']

def add_to_chroma(text, embeddings, client, collection):
    ids = [str(i) for i in list(range(len(embeddings)))]
    collection.add(documents=text, embeddings=embeddings, ids=ids)

def create_vectorb():
    client = chromadb.PersistentClient(path="RAGE_DB")
    collection_name = "RAGE-DB"
    try:
        client.delete_collection(name=collection_name)
    except:
        print("No collection by name: 'RAGE-DB' ")
    collection = client.get_or_create_collection(name=collection_name)
    return client, collection

# def run(uncleaned_text):
#     inputs = {'text_data': uncleaned_text}
#     results = TextProcessorCrew().crew().kickoff(inputs=inputs)