import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={GEMINI_API_KEY}"

class Model:
    def generate_content(self, prompt, retries=3, delay=10):
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        for attempt in range(retries):
            response = requests.post(GEMINI_URL, json=payload)
            if response.status_code == 429:
                print(f"Rate limited, waiting {delay}s... (attempt {attempt+1}/{retries})")
                time.sleep(delay)
                continue
            response.raise_for_status()
            data = response.json()
            return type("Response", (), {
                "text": data["candidates"][0]["content"]["parts"][0]["text"]
            })()
        raise Exception("Gemini API rate limit exceeded after retries")

model = Model()