from fastapi.testclient import TestClient
from app.main import app
from app.models import Model
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker
import pytest

# Create a test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Create tables before tests run
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after tests

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Test cases for uploading a model and retrieving models by name
# client = TestClient(app)

def test_upload_model(client):
    response = client.post("/app/models", 
                           params={
                               "model_name": "Test Model", 
                               "model_version": "v1", 
                               "model_accuracy": 0.95
                            },
                            files={"model_file": ("test_model.pkl", b"testing model content", "application/octet-stream")}
                        )
    
    response_json = response.json()
    print(response.json())  # Debugging output
    assert response.status_code == 201
    assert response_json["message"] == "Model was uploaded successfully"
    assert "model_id" in response_json

def test_get_models(client, db):
    response = client.get("/app/models")
    assert response.status_code == 200
    assert "models list" in response.json()

def test_get_model_by_name(client, db):
    from app.models import Model  # Import model within the test function
    test_model = Model(
        name="test_model",
        version="v1",
        accuracy=0.95,
        file_path="test_model.pkl"
    )
    db.add(test_model)
    db.commit()
    response = client.get("/app/models/test_model")
    assert response.status_code == 200
    assert response.json()["name"] == "test_model"

def test_get_unexisting_model(client):
    response = client.get("/app/models/non_existent_model")
    assert response.status_code == 404
    assert response.json() == {"detail": "Requested model not found"}