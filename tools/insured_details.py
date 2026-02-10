import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

def get_insured_details():
    """Get insured detail list from NowCerts"""
    url = f"{BASE_URL}/api/odata/InsuredDetailList"
    params = {
        "$count": "true",
        "$orderby": "changeDate DESC",
        "$skip": 0,
        "$top": 30
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.json())
    print("hello i am good")
    return response.json()
