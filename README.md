#   Simple Model Registry

Simple Model Registry is a FastAPI-based application for managing and storing machine learning models. It provides a simple API for uploading, retrieving, and listing models.

##  Features

-   Upload ML models with their associated metadata
-   Search and retrieve models by their specified name
-   Listing of all available models
-   SQLite database for storing ML models
-   Docker configuration for easy deployment
-   CI/CD pipeline with GitHub actions

##  Prerequisites

-   Python 3.9+
-   Docker and Docker Compose (for containerized deployment)
-   Git for version control

##  Getting Started

### Local Development

1.  Clone the repository:
```bash
git clone https://github.com/Spyro1322/my-model-registry.git
cd my-model-registry
```

2.  Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate (if on Windows, you shloud use venv\Scripts\activate)
```

3.  Install required dependencies
```bash
pip install -r requirements.txt
```

4.  Run the application:
```bash
uvicorn app. main:app --reload
```
Afterwards the application will be avaialble at `http://localhost:8000`.

### Docker Deployment

1.  Build and run the Docker container:
```bash
docker compose up --build
```
The application will be avaialble at `http://localhost:8000`.

##  API Endpoints

-   `POST /models`: Accepts an ML model file (e.g.,.pkl) and metadata (name, version, accuracy).
-   `GET /models`:  Returns metadata for all registered models.
-   `GET /models/{name}`:   Retrieves metadata for a specific model.

##  Project Structure

```
└── 📁my-model-registry
    └── 📁.github
        └── 📁workflows
            └── pipeline.yml
    └── 📁app
        └── __init__.py
        └── database.py
        └── main.py
        └── 📁models
        └── models.py
    └── 📁tests
        └── __init__.py
        └── test_main.py
    └── docker-compose.yml
    └── Dockerfile
    └── README.md
    └── requirements.txt
```

##  Testing

You can run the test using pytest:
```bash
pytest tests/
```

##  CI/CD Pipeline

The project includes a GitHub Actions workflow for CI/CD procedures. On each push to the master branch, it will:

1.  Run the test suite
2.  Build the Docker image
3.  Push the Docker image to a registry (configuration required)

## Contributing

Contributions are welcome! Please feel free to submit a pull request.


