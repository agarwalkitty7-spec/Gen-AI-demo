# webpage_utils.py

import requests
from bs4 import BeautifulSoup

def fetch_and_clean(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        texts = [tag.get_text(separator=' ', strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])]
        return " ".join(texts)
    except Exception as e:
        return None

def chunk_text(text, max_chunk_size=1000):
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i+max_chunk_size])
    return chunks
