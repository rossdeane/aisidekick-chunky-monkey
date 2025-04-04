import argparse
from web_scraper import scrape_urls
import os
from main import chunk_text, embed_texts, collection, client
from uuid import uuid4

def scrape_and_ingest(urls, target_id=None, output_file="scraped_content.txt"):
    """
    Scrape content from URLs and ingest it into the RAG system.
    
    Args:
        urls (list): List of URLs to scrape
        target_id (str, optional): The ID of the DOM element to extract
        output_file (str): The name of the output file
    """
    # Step 1: Scrape the content
    print(f"Scraping content from {len(urls)} URLs...")
    scrape_urls(urls, target_id, output_file)
    
    # Step 2: Read the scraped content
    print(f"Reading scraped content from {output_file}...")
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Step 3: Chunk the content
    print("Chunking content...")
    chunks = chunk_text(content)
    print(f"Created {len(chunks)} chunks")
    
    # Step 4: Embed and store the chunks
    print("Embedding and storing chunks...")
    embeddings = embed_texts([chunk for chunk in chunks])
    
    for i, e in enumerate(embeddings):
        collection.add(
            documents=[chunks[i]],
            embeddings=[e],
            ids=[str(uuid4())]
        )
    
    print(f"Successfully ingested {len(chunks)} chunks into the RAG system")

def main():
    parser = argparse.ArgumentParser(description='Scrape websites and ingest content into RAG system')
    parser.add_argument('--urls', nargs='+', required=True, help='List of URLs to scrape')
    parser.add_argument('--id', help='Optional DOM element ID to target')
    parser.add_argument('--output', default='scraped_content.txt', help='Output file name')
    
    args = parser.parse_args()
    
    scrape_and_ingest(args.urls, args.id, args.output)

if __name__ == "__main__":
    main() 