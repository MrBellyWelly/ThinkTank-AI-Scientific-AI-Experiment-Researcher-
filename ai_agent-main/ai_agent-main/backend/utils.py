import requests
import os

# SAVE_DIR = "downloads"
# os.makedirs(SAVE_DIR, exist_ok=True)

def save_pdf(url):
    file_name = os.path.basename(url)
    save_path = os.path.join(os.path.dirname(__file__), 'downloads', file_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": url,  # Set referer to the same URL to avoid cross-site request blocking
        "Accept-Language": "en-US,en;q=0.9",
    }
    """Download and save a PDF file."""
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            # file_name = url.rstrip("/").split("/")[-1] or "downloaded_file.pdf"
            # file_path = os.path.join(SAVE_DIR, file_name)
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"✅ Downloaded: {save_path}")
            return save_path
        else:
            print(f"❌ Failed to download {url} (Status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return None
