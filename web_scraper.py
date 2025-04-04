import requests
from bs4 import BeautifulSoup
import argparse
import os
from urllib.parse import urlparse
import time
import random

def scrape_url(url, target_id=None, delay=1):
    """
    Scrape content from a URL, optionally targeting a specific DOM element by ID.
    
    Args:
        url (str): The URL to scrape
        target_id (str, optional): The ID of the DOM element to extract
        delay (int): Delay between requests in seconds to be polite
        
    Returns:
        str: The scraped content
    """
    # Add a random delay to be polite to servers
    time.sleep(delay + random.random())
    
    try:
        # Set a user agent to identify our scraper
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # If a target ID is provided, extract only that element
        if target_id:
            target_element = soup.find(id=target_id)
            if target_element:
                return target_element.get_text(separator=' ', strip=True)
            else:
                print(f"Warning: Element with ID '{target_id}' not found on {url}")
                # Fall back to extracting the main content
                return extract_main_content(soup)
        else:
            # Extract the main content if no specific ID is provided
            return extract_main_content(soup)
            
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return f"Error scraping {url}: {str(e)}"

def extract_main_content(soup):
    """
    Extract the main content from a page, removing navigation, headers, footers, etc.
    
    Args:
        soup (BeautifulSoup): The parsed HTML
        
    Returns:
        str: The extracted content
    """
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
        script.extract()
    
    # Get the text
    text = soup.get_text(separator=' ', strip=True)
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Remove blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def scrape_urls(urls, target_id=None, output_file="scraped_content.txt"):
    """
    Scrape multiple URLs and save the content to a file.
    
    Args:
        urls (list): List of URLs to scrape
        target_id (str, optional): The ID of the DOM element to extract
        output_file (str): The name of the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, url in enumerate(urls):
            print(f"Scraping {i+1}/{len(urls)}: {url}")
            
            # Add a separator between different pages
            if i > 0:
                f.write("\n\n" + "="*80 + "\n\n")
            
            # Add the URL as a header
            f.write(f"SOURCE: {url}\n\n")
            
            # Scrape and write the content
            content = scrape_url(url, target_id)
            f.write(content)
    
    print(f"Scraping complete. Content saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Web scraper for RAG content collection')
    parser.add_argument('--urls', nargs='+', required=True, help='List of URLs to scrape')
    parser.add_argument('--id', help='Optional DOM element ID to target')
    parser.add_argument('--output', default='scraped_content.txt', help='Output file name')
    
    args = parser.parse_args()
    
    scrape_urls(args.urls, args.id, args.output)

if __name__ == "__main__":
    main() 