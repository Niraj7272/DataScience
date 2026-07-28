from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Load trained model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


# Define input data structure
class Passenger(BaseModel):
    pclass: int
    sex: int
    age: float
    sibsp: int
    parch: int
    fare: float
    embarked: int


# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to the Titanic Survival Prediction API!"
    }


# Prediction route
@app.post("/predict")
def predict(data: Passenger):

    # Create DataFrame from input data
    features = pd.DataFrame(
        [[
            data.pclass,
            data.sex,
            data.age,
            data.sibsp,
            data.parch,
            data.fare,
            data.embarked
        ]],
        columns=[
            "pclass",
            "sex",
            "age",
            "sibsp",
            "parch",
            "fare",
            "embarked"
        ]
    )

    # Scale input data
    scaled_data = scaler.transform(features)

    # Make prediction
    prediction = model.predict(scaled_data)[0]

    # Get probability of survival
    probability = model.predict_proba(scaled_data)[0][1]

    # Return result
    return {
        "survived": int(prediction),
        "survival_probability": round(float(probability), 2)
    }