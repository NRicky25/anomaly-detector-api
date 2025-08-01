from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Try .env API_KEY first, fallback to GitHub Actions secret
API_KEY = os.getenv("API_KEY") or os.getenv("WORKFLOW_API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return x_api_key