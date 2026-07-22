import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("Insurance Charge Prediction website")
st.write("Enter the details to predict insurance charges")

age = st.slider('Age',18,100,30)
sex = st.selectbox("Sex",['female','male'])
bmi = st.slider("BMI",10.0,50.0,25.0)
children = st.slider("Number of Children",0,10,0)
smoker = st.selectbox("Smoker",['Yes','No'])
region = st.selectbox("Region",['northeast','northwest','southeast','southwest'])

data = pd.read_csv('insurance.csv')

x = data.drop(columns=['charges'])
y = data['charges']

x = pd.get_dummies(
    x,
    columns=['region'],
    drop_first=True,
    dtype=int
)

x['sex'] = x['sex'].map({
    'female': 1,
    'male' : 0
})

x['smoker'] = x['smoker'].map({
    'yes': 1,
    'no' : 0
})

x['age_smoker'] = x['age'] * x['smoker']
x['bmi_smoker'] = x['bmi'] * x['smoker']

model = LinearRegression()

model.fit(x,y)

input_data = pd.DataFrame({
    'age':[age],
    'sex' : [1 if sex =='female' else 0],
    'bmi' : [bmi],
    'children' : [children],
    'smoker' : [1 if smoker=='yes' else 0],
    'region_northwest' : [1 if region=='northwest' else 0],
    'region_southeast' : [1 if region=='southeast' else 0],
    'region_southwest' : [1 if region=='southwest' else 0]
})

input_data['age_smoker'] = (input_data['age'] * input_data['smoker'])
input_data['bmi_smoker'] = (input_data['bmi'] * input_data['smoker'])

input_data = input_data[x.columns]


if st.button("Predict Charges"):
    prediction = model.predict(input_data)[0]
    st.success(f"The total predicted insurance charge is : ${prediction:.2f}")
