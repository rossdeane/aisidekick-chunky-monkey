# Web Scraper and RAG System

This project combines a web scraper with a Retrieval-Augmented Generation (RAG) system to create an AI-powered FAQ bot that can answer questions based on content scraped from websites.

## Setup

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Web Scraper

The web scraper can extract content from multiple URLs and save it to a text file:

```bash
python web_scraper.py --urls https://example.com https://example.org --id main-content --output scraped_content.txt
```

Arguments:

- `--urls`: List of URLs to scrape (required)
- `--id`: Optional DOM element ID to target
- `--output`: Output file name (default: scraped_content.txt)

### Scrape and Ingest into RAG

To scrape content and immediately ingest it into the RAG system:

```bash
python scrape_and_rag.py --urls https://example.com https://example.org --id main-content --output scraped_content.txt
```

### RAG System

To use the RAG system directly with a text file:

```bash
python main.py
```

This will prompt you to enter a question, and the system will search for relevant information in the ingested content and generate an answer.

## How It Works

1. **Web Scraping**: The scraper extracts content from the specified URLs, optionally targeting a specific DOM element by ID.
2. **Content Processing**: The scraped content is saved to a text file and then chunked into smaller pieces.
3. **Embedding**: Each chunk is embedded using OpenAI's embedding model.
4. **Storage**: The embeddings are stored in a ChromaDB vector database.
5. **Retrieval**: When a question is asked, the system retrieves the most relevant chunks from the database.
6. **Generation**: The retrieved chunks are used as context for the OpenAI model to generate an answer.

## Notes

- The web scraper includes polite delays between requests to avoid overwhelming servers.
- The RAG system uses OpenAI's text-embedding-3-small model for embeddings and gpt-4-0125-preview for generating answers.
- The ChromaDB database is stored in the `./chroma_data` directory.
