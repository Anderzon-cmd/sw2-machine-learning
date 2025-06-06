from contextlib import asynccontextmanager
import os
from typing import Union

from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd

from app.schemas.predict_cancelled import PredictCancelledRequest

model=None
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    root_path = os.getcwd()
    model_path = os.path.join(root_path, "app", "models", "cancelled-rforest_model.pkl")
    if not os.path.exists(model_path):
        raise RuntimeError(
            "Model file not found. Please ensure the model is available at the specified path."
        )
    model = joblib.load(model_path)
    print("Model loaded successfully.")
    yield
    print("Shutting down the application.")
    

app = FastAPI(lifespan=lifespan)

@app.post("/predict-cancelled")
def predict(predict_request: PredictCancelledRequest):
    features = pd.DataFrame([predict_request.model_dump()])
    prediction = model.predict(features)

    return {"prediction": int(prediction[0])}


    