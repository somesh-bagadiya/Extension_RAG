from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import Document, Settings
from llama_index.core.llms import ChatMessage, MessageRole
from uuid import uuid4
import os
import re
import chromadb
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
embed_model = None
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
print(nvidia_api_key)

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
    print("process_text called")
    uncleaned_text = data.content
    get_nims_embeddings(uncleaned_text)
    return {"message": "Text received successfully.", "content_length": len(data.content)}

@app.post("/process-query/")
async def process_query(data: TextData):
    print("process_query called")
    user_query = data.content
    response_message = f"**Prompt: {user_query}**"
    context = retrieve_query_related_embeddings(user_query)
    print(context)
    response = generate_response(context, user_query)
    response = response.__str__()
    print(type(response))
    response = response.replace("assistant: ", "")
    response_message = response_message + f"\n\n**Response:** {response}"
    return {"message": response_message}

def generate_response(context, user_query):
    global nvidia_api_key
    llm = NVIDIA(model='nvidia/llama-3.1-nemotron-70b-instruct', nvidia_api_key=nvidia_api_key)
    Settings.llm = llm
    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM, content=("You are a concise, helpful assistant. Use the provided context to answer user queries with brief yet thorough responses. " + str(context))
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(user_query),
        ),
    ]
    response = llm.chat(messages)
    print(response)
    return response

def clean_text(text):
    text = re.sub(r'(\b\w+\b)(\s+\1)+', r'\1', text)
    text = re.sub(r'\bundefined\b', '', text)  # Remove "undefined" instances
    text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
    cleaned_lines = [line.strip() for line in text.splitlines() if line.strip() and not re.match(r'^[\W_]+$', line)]
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text.strip()

def get_nims_embeddings(uncleaned_text):
    global embed_model, nvidia_api_key
    embed_model = NVIDIAEmbedding(model="nvidia/nv-embedqa-mistral-7b-v2", nvidia_api_key=nvidia_api_key)
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