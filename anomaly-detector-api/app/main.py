from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator
import joblib
import numpy as np
import os
from app.utils import verify_api_key
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

app = FastAPI(
    title="Anomaly Detector API",
    description="API to detect fraud/anomalies in transactions using Isolation Forest model",
    version="1.0.0"
)

# Load model and scaler once when app starts
model = joblib.load("model/isolation_forest.joblib")
scaler = joblib.load("model/scaler.joblib")

class Transaction(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float; Amount: float

    class Config:
        extra = Extra.allow

    @field_validator("Amount")
    def check_amount(cls, value):
        if value < 0:
            raise ValueError("Amount cannot be negative")
        return value

@app.post("/predict/")
def predict(transaction: Transaction, api_key: str = Depends(verify_api_key)):
    try:
        values = np.array([[getattr(transaction, f"V{i}") for i in range(1, 29)] + [transaction.Amount]])
        values_scaled = scaler.transform(values)
        result = model.predict(values_scaled)
        prediction = "OK" if result[0] == 1 else "FRAUD"
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")
