from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle

# Load the scaler and model
scaler = pickle.load(open("../models/scaler.pkl",'rb'))
model = pickle.load(open("../models/knn_model.pkl",'rb'))

app = FastAPI(title='Life Expectancy Prediction API')

# Input schema
class InputData(BaseModel):
    Year: int
    Status: int
    Adult_Mortality: float
    Infant_Deaths: float
    Alcohol: float
    percentage_expenditure: float
    Hepatitis_B: float
    Measles: float
    BMI: float
    under_five_deaths: float
    Polio: float
    Total_expenditure: float
    Diphtheria: float
    HIV_AIDS: float
    GDP: float
    Population: float
    thinness_1_19_years: float
    thinness_5_9_years: float
    Income_composition_of_resources: float
    Schooling: float

@app.get('/')
def home():
    return{
        "message": "Welcome to the Life Expectancy Prediction API!"
    }

@app.post("/predict")
def predict(data:InputData):
    input_array = np.array([[
        data.Year,
        data.Status == 0 if data.Status == "developing" else 1,
        data.Adult_Mortality,
        data.Infant_Deaths,
        data.Alcohol,
        data.percentage_expenditure,
        data.Hepatitis_B,
        data.Measles,
        data.BMI,
        data.under_five_deaths,
        data.Polio,
        data.Total_expenditure,
        data.Diphtheria,
        data.HIV_AIDS,
        data.GDP,
        data.Population,
        data.thinness_1_19_years,
        data.thinness_5_9_years,
        data.Income_composition_of_resources,
        data.Schooling
    ]])

    scaled = scaler.transform(input_array)
    prediction = model.predict(scaled)

    return {"life_expectancy": float(prediction[0])}
    