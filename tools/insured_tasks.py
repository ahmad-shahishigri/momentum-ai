import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

def get_insured_tasks(insured_database_ids: list[str]):
    """Get insured tasks"""
    url = f"{BASE_URL}/api/Insured/InsuredTasks"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "InsuredDataBaseId": insured_database_ids
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
