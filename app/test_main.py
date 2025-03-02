from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_model():
    response = client.post("/models", 
                           data={"model_name": "Test Model", 
                                 "model_version": "v1", 
                                 "model_accuracy": 0.95
                                },
                            files={"model_file": ("test_model.pkl", b"testing model content", "application/octet-stream")}
                        )
    assert response.status_code == 201
    assert response.json() == {"message": "Model was uploaded successfully", "id": "test_id"}

def test_get_models():
    response = client.get("/models")
    assert response.status_code == 200
    assert response.json() == {"models list": []}

def test_get_model_by_name():
    response = client.get("/models/test_model")
    assert response.status_code == 200
    assert response.json() == {"name": "test_model"}

def test_get_unexisting_model():
    response = client.get("/models/non_existent_model")
    assert response.status_code == 404
    assert response.json() == {"message": "Requested model not found"}