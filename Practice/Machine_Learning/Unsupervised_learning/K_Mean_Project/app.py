import streamlit as st
import pandas as pd
import numpy as np
import joblib

kmeans = joblib.load('kmeans_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title('Customer Segmentation using K-Means Clustering')
st.write('Enter customerd details to predict their segment.')



age = st.number_input('Age', min_value=18, max_value=100, value=30)
income = st.number_input('Annual Income (k$)', min_value=0, max_value=200000, value=50)
total_spending = st.number_input('Total Spending', min_value=0, max_value=5000, value=20)
num_web_purchases = st.number_input('Number of Web Purchases', min_value=0, max_value=100, value=5)
num_store_purchases = st.number_input('Number of Store Purchases', min_value=0, max_value=100, value=3)
num_web_visits = st.number_input('Number of Web Visits', min_value=0, max_value=100, value=10)
recency = st.number_input('Recency (days since last purchase)', min_value=0, max_value=365, value=30)

input_data = pd.DataFrame({
    'Age': [age],
    'Income': [income],
    'Total_Spending': [total_spending],
    'NumWebPurchases': [num_web_purchases],
    'NumStorePurchases': [num_store_purchases],
    'NumWebVisitsMonth': [num_web_visits],
    'Recency': [recency]
})

st.write("Input Data:")
st.write(input_data)



input_scaled = scaler.transform(input_data)

st.write("Scaled Input:")
st.write(input_scaled)

if st.button('Predict Segment'):
    cluster = kmeans.predict(input_scaled)
    st.write(f'The predicted customer segment is: Cluster {cluster[0]}')