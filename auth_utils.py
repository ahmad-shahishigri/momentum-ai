import os
import requests
from dotenv import load_dotenv
from auth_utils import get_access_token

load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

def get_access_token(api_key: str) -> str:
    token = get_access_token(API_KEY)
    """Get insured detail list from NowCerts. This does not need any input parameter"""
    url = f"{BASE_URL}/api/odata/InsuredDetailList"
    params = {
        "$count": "true",
        "$orderby": "changeDate DESC",
        "$skip": 0,
        "$top": 1
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()
