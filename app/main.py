from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
import uuid

app = FastAPI()

@app.post("/app/models")
async def upload_model(model_name: str, model_version:str, model_accuracy: float, model_file: UploadFile = File(...)):
    db = database.SessionLocal()
    try:
        if db.query(models.Model).filter(models.Model.name == model_name, models.Model.version == model_version).first():
            raise HTTPException(status_code=409, detail="Model already exists")

        model_id = str(uuid.uuid4())
        file_location = f"/app/models/{model_id}_{model_file.filename}"
        with open(file_location, "wb+") as file_object:
            await file_object.write(model_file.file.read())

        new_model = models.Model(id=model_id, name=model_name, version=model_version, accuracy=model_accuracy, file_path=file_location)

        db.add(new_model)
        db.commit()
        db.refresh(new_model)

        return JSONResponse(status_code=201, content={"message": "Model was uploaded successfully", "id": new_model.id})
    
    finally:
        db.close()

@app.get("/app/models")
async def get_models():
    db = database.SessionLocal()
    try:
        models_catalog = db.query(models.Model).all()
        return JSONResponse(status_code=200, content={"models list": [model.__dict__ for model in models_catalog]})
    finally:
        db.close()

@app.get("/app/models/{model_name}")
async def get_model_by_name(model_name: str):
    db = database.SessionLocal()
    try:
        model = db.query(models.Model).filter(models.Model.name == model_name).first()
        if model is None:
            raise HTTPException(status_code=404, detail="Requested model not found")
        return JSONResponse(status_code=200, content=model.__dict__)
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)