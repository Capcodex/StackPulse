import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.list() # Using generic list if available or raw request
    for m in response:
        print(m.name)
except Exception as e:
    print(f"Error: {e}")
