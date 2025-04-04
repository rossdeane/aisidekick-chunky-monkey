# AI Sidekick Chunky Monkey

A RAG-based FAQ bot using OpenAI and ChromaDB for intelligent question answering.

## Requirements

- Python 3.8 or higher
- OpenAI API key

## Setup

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   make install
   ```
4. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
5. Edit `.env` and add your OpenAI API key

## Usage

1. Prepare your FAQ content in `example_faq.txt`
2. Run the bot:
   ```bash
   make run
   ```

## Development

- Clean temporary files: `make clean`
- Run tests: `make test`
