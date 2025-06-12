

from app.schemas.predict_cancelled import PredictCancelledRequest
from contextlib import asynccontextmanager
from app.schemas.predict_dest_popular import PredictDestPopular
from fastapi import FastAPI
from keras.models import load_model
from typing import Union
from fastapi import HTTPException
from fastapi import HTTPException
from sklearn.preprocessing import StandardScaler
from fastapi.middleware.cors import CORSMiddleware

import joblib
import os
import pandas as pd


model=None
model_dest=None

@asynccontextmanager
async def load_model_cancelled():
    global model
    root_path = os.getcwd()
    model_path = os.path.join(root_path, "app", "models", "cancelled_rforest_model.pkl")
    if not os.path.exists(model_path):
        raise RuntimeError(
            "Model cancelled travel file not found. Please ensure the model is available at the specified path."
        )
    model = joblib.load(model_path)
    print("Model cancelled travel loaded successfully.")
    yield
    

@asynccontextmanager
async def load_model_dest_popular():
    global model_dest
    root_path = os.getcwd()
    model_path = os.path.join(root_path, "app", "models", "model_dest_popular.keras")
    if not os.path.exists(model_path):
        raise RuntimeError(
            "Model dest travel file not found. Please ensure the model is available at the specified path."
        )
    model_dest = load_model(model_path,compile=False)
    print("Model dest travel loaded successfully.")
    yield
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with load_model_cancelled(),load_model_dest_popular():
        yield
        print("Application shutdown")

    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/predict-cancelled")
def predict(request: PredictCancelledRequest):
    features = pd.DataFrame([request.model_dump()])
    prediction = model.predict(features)

    return {"prediction": int(prediction[0])}

@app.post("/predict-dest-popular")
def predict_dest_popular(request:PredictDestPopular):
    encode_dest = pd.read_csv(os.path.join(os.getcwd(), 'app', 'encoded', 'dest_airport_encoded.csv'))
    encode_origin = pd.read_csv(os.path.join(os.getcwd(), 'app', 'encoded', 'origin_airport_encoded.csv'))

    scaler=joblib.load(os.path.join(os.getcwd(), "app", "scalers", "scaler_dest_popular.pkl"))

    origin_row = encode_origin[encode_origin['ORIGIN'] == request.origin]
    origin_row.values
    if origin_row.empty:
        raise HTTPException(status_code=404, detail="Origin airport not found")

    
    dest_row = encode_dest[encode_dest['DEST'] == request.dest]
    if dest_row.empty:
        raise HTTPException(status_code=404, detail="Destination airport not found")
    
    input_normalized=pd.DataFrame([[
        request.month,
        request.day_week,
        request.holiday,
        request.vacation,
        request.important_event,
        origin_row.values[0][1],
        dest_row.values[0][1]
        ]],
        columns=['MONTH','DAY_WEEK','HOLIDAY','VACATION','IMPORTANT_EVENT','ORIGIN_ENCONDED','DEST_ENCONDED']
        )
    
    input_normalized[['ORIGIN_ENCONDED', 'DEST_ENCONDED', 'DAY_WEEK','MONTH']]=scaler.transform(input_normalized[['ORIGIN_ENCONDED', 'DEST_ENCONDED', 'DAY_WEEK','MONTH']])
    print(input_normalized)
    

    pred=model_dest.predict(input_normalized)
    return {
        'probability': round(float(pred[0][0]), 4),
        'popular': int(pred[0][0] > 0.5)
    }






    