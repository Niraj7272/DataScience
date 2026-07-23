from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

#Load model and scaler using joblib
model = joblib.load('multiple_linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

class InputData(BaseModel) :
    interest_rate : float
    unemployment_rate : float

@app.post('/predict')
def predict(data: InputData):
    x = np.array([[data.interest_rate, data.unemployment_rate]])
    x_scaled = scaler.transform(x)
    prediction = model.predict(x_scaled)[0]
    return {"index_price": round(float(prediction),2)}
    