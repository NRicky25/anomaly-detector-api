import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model():
    df = pd.read_csv("data/creditcard.csv")

    # Fix typo: should be 'columns' not 'colunms'
    X = df.drop(columns=['Time', 'Class'])

    scaler = StandardScaler()

    # Fix variable name: it was lowercase 'x' but you defined 'X'
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest model
    model = IsolationForest(contamination=0.0017, random_state=42)
    model.fit(X_scaled)

    # Fix typo: 'exits_ok' should be 'exist_ok'
    os.makedirs("model", exist_ok=True)

    # Save the model and scaler files
    joblib.dump(model, "model/isolation_forest.joblib")
    joblib.dump(scaler, "model/scaler.joblib")

    print("Model and scaler saved successfully")

# To run training if this script is executed directly:
if __name__ == "__main__":
    train_model()
