# groq_client.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "openai/gpt-oss-20b"

def stream_groq_response(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False  # disable streaming for now
    }

    with httpx.Client(timeout=30) as client:
        response = client.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        answer = "".join(choice["message"]["content"] for choice in result.get("choices", []))
        yield answer
