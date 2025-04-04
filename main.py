# Simple RAG pipeline for an AI FAQ bot using OpenAI + ChromaDB
# Note: this is a basic script for dev/test purposes

from openai import OpenAI
import chromadb
from chromadb.config import Settings
from uuid import uuid4
import os
from dotenv import load_dotenv
import pathlib

# Get absolute path to .env file
env_path = pathlib.Path(__file__).parent.absolute() / '.env'
print(f"Looking for .env at: {env_path}")
print(f".env file exists: {env_path.exists()}")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path, verbose=True)

# Debug: Print environment variable
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if not api_key:
    print("Warning: OPENAI_API_KEY environment variable not found!")

client = OpenAI(api_key=api_key)

# --- Setup vector DB ---
# Updated to use the new ChromaDB client initialization
chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection(name="business_faq")

# --- Step 1: Ingest content ---
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Example usage
with open("carhood_content.txt", "r") as f:
    content = f.read()

chunks = chunk_text(content)

# --- Step 2: Embed and store ---
def embed_texts(texts):
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    return [item.embedding for item in response.data]

embeddings = embed_texts([chunk for chunk in chunks])

for i, e in enumerate(embeddings):
    collection.add(
        documents=[chunks[i]],
        embeddings=[e],
        ids=[str(uuid4())]
    )

# --- Step 3: Answer a query ---
def search_and_respond(query):
    query_embedding = client.embeddings.create(input=[query], model="text-embedding-3-small").data[0].embedding
    results = collection.query(query_embeddings=[query_embedding], n_results=5)

    context = "\n\n".join(results['documents'][0])

    prompt = f"""
    You are a friendly and helpful assistant for a small business.
    
    A customer asked: "{query}"

    Based on the following information, answer clearly and helpfully:
    ---
    {context}
    ---
    """

    response = client.chat.completions.create(model="gpt-4-0125-preview",
    messages=[{"role": "user", "content": prompt}])

    return response.choices[0].message.content

# --- Test it ---
if __name__ == "__main__":
    user_question = input("Customer: ")
    answer = search_and_respond(user_question)
    print("Bot:", answer)
