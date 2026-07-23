import streamlit as st
import requests

st.title("Index Price Predictor")

interest_rate = st.number_input("Interest Rate (%)")
unemployment_rate = st.number_input("Unemployment Rate (%)")

if st.button("predict"):
    response = requests.post(
        "http://localhost:8000/predict",
        json={"interest_rate": interest_rate, "unemployment_rate": unemployment_rate}
    )
    result = response.json()
    st.success(f"Predicted Index Price: **{result['index_price']}**")
    