# Simple RAG pipeline for an AI FAQ bot using OpenAI + ChromaDB
# Note: this is a basic script for dev/test purposes

import openai
import chromadb
from chromadb.config import Settings
from uuid import uuid4
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Setup vector DB ---
chroma_client = chromadb.Client(Settings(persist_directory="./chroma_data", chroma_db_impl="duckdb+parquet"))
collection = chroma_client.get_or_create_collection(name="business_faq")

# --- Step 1: Ingest content ---
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Example usage
with open("example_faq.txt", "r") as f:
    content = f.read()

chunks = chunk_text(content)

# --- Step 2: Embed and store ---
def embed_texts(texts):
    return openai.Embedding.create(input=texts, model="text-embedding-3-small")['data']

embeddings = embed_texts([chunk for chunk in chunks])

for i, e in enumerate(embeddings):
    collection.add(
        documents=[chunks[i]],
        embeddings=[e['embedding']],
        ids=[str(uuid4())]
    )

# --- Step 3: Answer a query ---
def search_and_respond(query):
    query_embedding = openai.Embedding.create(input=[query], model="text-embedding-3-small")['data'][0]['embedding']
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

    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

# --- Test it ---
if __name__ == "__main__":
    user_question = input("Customer: ")
    answer = search_and_respond(user_question)
    print("Bot:", answer)
