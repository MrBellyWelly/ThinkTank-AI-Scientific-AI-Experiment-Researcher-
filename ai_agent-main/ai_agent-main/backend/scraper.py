import requests
import os
from utils import save_pdf
from langchain_community.document_loaders import ArxivLoader

def is_pdf_link(link):
    """Check if the link is a direct PDF file."""
    try:
        # Try HEAD request first
        response = requests.head(link, allow_redirects=True, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        if content_type == 'application/pdf' or link.endswith('.pdf'):
            return True
        
        # Fallback to GET request and check file signature
        response = requests.get(link, stream=True, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        
        # Check content type or PDF signature
        if content_type == 'application/pdf':
            return True
        
        # Read the first 4 bytes to check the PDF signature "%PDF"
        first_bytes = response.raw.read(4)
        return first_bytes == b'%PDF'
    
    except requests.RequestException:
        return False

def download_papers(links):
    """Download PDF files from links."""
    downloaded_files = []
    for link in links:
        try:
            file_path = save_pdf(link)
            if file_path:
                downloaded_files.append(file_path)
        except Exception as e:
            print(f"Failed to download {link}: {e}")
    return downloaded_files


def search_and_load_papers(query, max_results=5):
    """Search and load papers from arXiv based on a query."""
    loader = ArxivLoader(
        query=query,
        max_results=max_results
    )
    documents = loader.load()

    return documents