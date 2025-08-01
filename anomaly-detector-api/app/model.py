import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model():
    df = pd.read_csv("data/creditcard.csv")

    X = df.drop(colunms = ['Time', 'Class'])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(x)

    # Train Isolateion Forest
    model = IsolationForest(contamination=0.0017, random_state=42)
    model.fit(X_scaled)

    #Save model and scaler to joblib
    os.makedirs("model", exits_ok=True)
    joblib.dump(model, "model/isolation_forest.joblib")
    joblib.dump(scaler, "model/scaler.joblib")

    print("Model and scaler saved successfully")