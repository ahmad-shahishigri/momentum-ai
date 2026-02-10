import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

def insert_insured_no_override(payload: dict):
    """Insert insured without override"""
    url = f"{BASE_URL}/api/Insured/OnlyInsertInsured"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
