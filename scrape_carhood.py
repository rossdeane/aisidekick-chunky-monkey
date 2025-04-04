from scrape_and_rag import scrape_and_ingest

# List of car manufacturer URLs to scrape
car_urls = [
    'https://www.carhood.com/alfa-romeo/',
    'https://www.carhood.com/audi/',
    'https://www.carhood.com/bmw',
    'https://www.carhood.com/fiat/',
    'https://www.carhood.com/ford/',
    'https://www.carhood.com/honda/',
    'https://www.carhood.com/jaguar/',
    'https://www.carhood.com/lotus/',
    'https://www.carhood.com/mazda/',
    'https://www.carhood.com/mercedes/',
    'https://www.carhood.com/mg/',
    'https://www.carhood.com/mini/',
    'https://www.carhood.com/nissan/',
    'https://www.carhood.com/porsche/',
    'https://www.carhood.com/saab/',
    'https://www.carhood.com/toyota/',
    'https://www.carhood.com/volkswagen/',
    'https://www.carhood.com/volvo/'
]

if __name__ == "__main__":
    print(f"Starting to scrape {len(car_urls)} car manufacturer pages from carhood.com...")
    
    # Scrape the content and ingest it into the RAG system
    # We're targeting the main content area, which typically has ID 'content' or 'main-content'
    # If this doesn't work, we can try without specifying an ID
    scrape_and_ingest(
        urls=car_urls,
        target_id="main-content",  # Try with 'content' first, can be changed if needed
        output_file="carhood_content.txt"
    )
    
    print("Scraping and ingestion complete!") 