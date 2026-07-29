import streamlit as st
import requests

st.set_page_config(page_title="Life Expectancy Predictor")
st.title("Life Expectancy Prediction App")

st.write("Enter the details below to predict life expectancy:")

Year = st.number_input("Year", min_value=2000, max_value=2020, value=2015)
Status = st.selectbox("Status", options=["Developing", "Developed"])
Status = 0 if Status == "Developing" else 1
Adult_Mortality = st.number_input("Adult Mortality")
infant_deaths = st.number_input("Infant Deaths")
Alcohol = st.number_input("Alcohol Consumption")
percentage_expenditure = st.number_input("Health Expenditure(%)")
Hepatitis_B = st.number_input("Hepatitis B Immunization (%)")
Measles = st.number_input("Measles Cases")
BMI = st.number_input("BMI")
under_five_deaths = st.number_input("Under Five Deaths")
Polio = st.number_input("Polio Immunization (%)")
Total_expenditure = st.number_input("Total Expenditure (%)")
Diphtheria = st.number_input("Diphtheria Immunization (%)")
HIV_AIDS = st.number_input("HIV/AIDS Deaths")
GDP = st.number_input("GDP")
Population = st.number_input("Population")
thinness_1_19_years = st.number_input("Thinness 1-19 years")
thinness_5_9_years = st.number_input("Thinness 5-9 years")
Income_composition_of_resources = st.number_input("Income Composition of Resources")
Schooling = st.number_input("Schooling (years)")

if st.button("Predict"):

    url = "http://127.0.0.1:8000/predict"

    payload = {
        "Year": Year,
        "Status": Status,
        "Adult_Mortality": Adult_Mortality,
        "Infant_Deaths": infant_deaths,
        "Alcohol": Alcohol,
        "percentage_expenditure": percentage_expenditure,
        "Hepatitis_B": Hepatitis_B,
        "Measles": Measles,
        "BMI": BMI,
        "under_five_deaths": under_five_deaths,
        "Polio": Polio,
        "Total_expenditure": Total_expenditure,
        "Diphtheria": Diphtheria,
        "HIV_AIDS": HIV_AIDS,
        "GDP": GDP,
        "Population": Population,
        "thinness_1_19_years": thinness_1_19_years,
        "thinness_5_9_years": thinness_5_9_years,
        "Income_composition_of_resources": Income_composition_of_resources,
        "Schooling": Schooling
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Life Expectancy: {result['life_expectancy']:.2f} years")
            
    else:
        st.error("Error connecting to the API")