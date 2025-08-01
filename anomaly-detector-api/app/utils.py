from fastapi import Header, HTTPException, status
from dotenv import load_dotenv
import os
from pathlib import Path

if not os.getenv("CI"):
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")

if not API_KEY:
     raise RuntimeError("API_KEY environment variable not set. Please ensure it's configured in .env for local development or GitHub Secrets for CI.")

def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency to verify the API key provided in the 'x-api-key' header.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key")
    return x_api_key