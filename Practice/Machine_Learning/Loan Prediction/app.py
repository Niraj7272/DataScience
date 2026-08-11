"""
Loan Approval Prediction - Streamlit Frontend
Loads the trained model bundle (best_loan_model.pkl) produced by model.ipynb
and lets a user enter applicant details to get a loan approval prediction.
"""

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Loan Approval Predictor",
    page_icon="💰",
    layout="centered",
)


# Load model bundle
@st.cache_resource
def load_bundle(path: str = "best_loan_model.pkl"):
    return joblib.load(path)


try:
    bundle = load_bundle()
except FileNotFoundError:
    st.error(
        "Model file `best_loan_model.pkl` not found. "
        "Run `model.ipynb` first to train and save the model."
    )
    st.stop()

model = bundle["model"]
scaler = bundle["scaler"]
label_encoder = bundle["label_encoder"]
feature_cols = bundle["feature_cols"]
employment_classes = bundle["employment_status_classes"]
model_name = bundle["model_name"]


# Header
st.title("💰 Loan Approval Predictor")
st.write(
    "Enter applicant details below to predict whether a loan application "
    "is likely to be **approved** or **rejected**."
)
st.caption(f"Serving model: **{model_name}** (trained in `model.ipynb`)")

st.divider()


# Input form

with st.form("loan_form"):
    st.subheader("Applicant Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=35, step=1)
        income = st.number_input(
            "Annual Income ($)", min_value=0, max_value=1_000_000, value=60000, step=1000
        )
        credit_score = st.number_input(
            "Credit Score", min_value=300, max_value=850, value=650, step=1
        )

    with col2:
        loan_amount = st.number_input(
            "Loan Amount ($)", min_value=0, max_value=1_000_000, value=20000, step=500
        )
        loan_term = st.selectbox(
            "Loan Term (months)", options=[12, 24, 36, 48, 60], index=2
        )
        employment_status = st.selectbox("Employment Status", options=employment_classes)

    submitted = st.form_submit_button("Predict Loan Approval", use_container_width=True)

# Prediction

if submitted:
    employment_encoded = label_encoder.transform([employment_status])[0]

    input_df = pd.DataFrame(
        [[age, income, credit_score, loan_amount, loan_term, employment_encoded]],
        columns=feature_cols,
    )

    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    proba = (
        model.predict_proba(input_scaled)[0]
        if hasattr(model, "predict_proba")
        else None
    )

    st.divider()
    st.subheader("Prediction Result")

    if prediction == 1:
        st.success(" **Loan Approved**")
    else:
        st.error(" **Loan Rejected**")

    if proba is not None:
        approve_prob = proba[1] * 100
        reject_prob = proba[0] * 100

        st.write("**Prediction Confidence**")
        c1, c2 = st.columns(2)
        c1.metric("Approval Probability", f"{approve_prob:.1f}%")
        c2.metric("Rejection Probability", f"{reject_prob:.1f}%")

        st.progress(min(max(approve_prob / 100, 0.0), 1.0))

    with st.expander("See input summary"):
        st.dataframe(
            input_df.rename(columns={"Employment_Status_Encoded": "Employment_Status (encoded)"}),
            use_container_width=True,
        )

st.divider()
st.caption(
    "This tool provides an automated estimate based on a machine learning model "
    "trained on historical data. It is not financial advice and should not be "
    "used as the sole basis for a real lending decision."
)