from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_transaction():
    response = client.post("/predict/", json={
        "V1": 0.1, "V2": -1.1, "V3": 0.5, "V4": -0.2, "V5": 0.3,
        "V6": 1.2, "V7": -0.5, "V8": 0.4, "V9": -1.3, "V10": 0.8,
        "V11": -0.6, "V12": 1.0, "V13": -0.7, "V14": 0.9, "V15": 0.0,
        "V16": -0.4, "V17": 1.1, "V18": -0.3, "V19": 0.2, "V20": 0.1,
        "V21": -0.9, "V22": 0.6, "V23": 0.3, "V24": -0.8, "V25": 0.5,
        "V26": -0.1, "V27": 0.7, "V28": -0.6, "Amount": 120.00
    })
    assert response.status_code == 200
    assert response.json()["prediction"] in ["OK", "FRAUD"]

def test_negative_amount():
    response = client.post("/predict/", json={"V1": 0.1, "V2": -1.1, "V3": 0.5, "V4": -0.2, "V5": 0.3,
        "V6": 1.2, "V7": -0.5, "V8": 0.4, "V9": -1.3, "V10": 0.8,
        "V11": -0.6, "V12": 1.0, "V13": -0.7, "V14": 0.9, "V15": 0.0,
        "V16": -0.4, "V17": 1.1, "V18": -0.3, "V19": 0.2, "V20": 0.1,
        "V21": -0.9, "V22": 0.6, "V23": 0.3, "V24": -0.8, "V25": 0.5,
        "V26": -0.1, "V27": 0.7, "V28": -0.6, "Amount": -10.00
        })
    assert response.status_code == 422 #Fail validation

def test_missing_field():
    data = {
        "V1": -1.3,
        # Missing V2–V28 and Amount
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 422  # Unprocessable Entity

def test_extremely_large_values():
    data = {f"V{i}": 1e10 for i in range(1, 29)}
    data["Amount"] = 1e10
    response = client.post("/predict/", json=data)
    assert response.status_code == 200


def test_boundary_values():
    data = {f"V{i}": 0.00001 for i in range(1, 29)}
    data["Amount"] = 0.01
    response = client.post("/predict/", json=data)
    assert response.status_code == 200

def test_string_instead_of_number():
    data = {f"V{i}": "not_a_number" for i in range(1, 29)}
    data["Amount"] = "ten"
    response = client.post("/predict/", json=data)
    assert response.status_code == 422 

def test_extra_field():
    data = {f"V{i}": 0.5 for i in range(1, 29)}
    data["Amount"] = 50.00
    data["extra"] = "unexpected"
    response = client.post("/predict/", json=data)
    assert response.status_code == 200

def test_all_zero_input():
    data = {f"V{i}": 0.0 for i in range(1, 29)}
    data["Amount"] = 0.0
    response = client.post("/predict/", json=data)
    assert response.status_code == 200
    assert response.json()["prediction"] in ["OK", "FRAUD"]

def test_high_precision_floats():
    data = {f"V{i}": 0.12345678901234567890 for i in range(1, 29)}
    data["Amount"] = 0.12345678901234567890
    response = client.post("/predict/", json=data)
    assert response.status_code == 200

def test_wrong_types_but_valid_json():
    data = {f"V{i}": None for i in range(1, 29)}
    data["Amount"] = None
    response = client.post("/predict/", json=data)
    assert response.status_code == 422