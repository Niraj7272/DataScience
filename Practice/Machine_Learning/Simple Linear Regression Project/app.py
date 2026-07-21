import streamlit as st
import joblib
import numpy as np

st.set_page_config(
    page_title="Height Prediction App",
    page_icon="📏",
    layout="centered"
)


model = joblib.load("simple_linear_regression_model.pkl")
scaler = joblib.load("scaler.pkl")


st.title(" Height Prediction using Simple Linear Regression")

st.write(
    """
    This application predicts a person's **Height**
    based on their **Weight** using a trained
    Simple Linear Regression model.
    """
)

st.divider()


weight = st.number_input(
    "Enter Weight (kg)",
    min_value=1.0,
    max_value=200.0,
    value=70.0,
    step=0.5
)


if st.button("Predict Height"):

    # Convert input to numpy array
    input_data = np.array([[weight]])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    st.success(f"Predicted Height: **{prediction[0]:.2f} cm**")

st.sidebar.header("Model Information")

st.sidebar.write("**Model:** Simple Linear Regression")

st.sidebar.write(f"**Coefficient:** {model.coef_[0]:.4f}")

st.sidebar.write(f"**Intercept:** {model.intercept_:.4f}")

st.sidebar.write(
    """
    **Input**
    - Weight (kg)

    **Output**
    - Height (cm)
    """
)

st.sidebar.success("Model Loaded Successfully")
