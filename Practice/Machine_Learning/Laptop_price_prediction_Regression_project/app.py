"""
Laptop Price Predictor - Streamlit App
---------------------------------------
Loads the model, scaler, encoder, and metadata saved by ml.ipynb
and lets the user pick laptop specs to get a predicted price.

Run with:
    streamlit run app.py

Make sure best_model.pkl, scaler.pkl, encoder.pkl, and meta.pkl are in the
same folder as this file (they are created by running ml.ipynb).
"""

import numpy as np
import pandas as pd
import streamlit as st
import joblib
from sklearn.preprocessing import PolynomialFeatures

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="centered")



# Load saved model + preprocessing objects (cached so it only loads once)
@st.cache_resource
def load_artifacts():
    model = joblib.load("best_model.pkl")
    scaler = joblib.load("scaler.pkl")
    encoder = joblib.load("encoder.pkl")
    meta = joblib.load("meta.pkl")
    return model, scaler, encoder, meta


try:
    model, scaler, encoder, meta = load_artifacts()
except FileNotFoundError:
    st.error(
        "Model files not found. Please run ml.ipynb first — it saves "
        "best_model.pkl, scaler.pkl, encoder.pkl, and meta.pkl into this folder."
    )
    st.stop()

cat_cols = meta["cat_cols"]
num_cols = meta["num_cols"]
options = meta["options"]
num_ranges = meta["num_ranges"]
ram_options = meta["ram_options"]
rom_options = meta["rom_options"]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("💻 Laptop Price Predictor")
st.write(
    f"This app predicts a laptop's price using a trained "
    f"**{meta['best_model_name']}** model. Fill in the specs below and click "
    f"**Predict Price**."
)

st.divider()

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
st.subheader("Laptop Specifications")

col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Brand", options["brand"])
    processor_brand = st.selectbox("Processor Brand", options["processor_brand"])
    ram = st.selectbox("RAM (GB)", ram_options, index=ram_options.index(8) if 8 in ram_options else 0)
    ram_type = st.selectbox("RAM Type", options["Ram_type"])
    rom = st.selectbox("Storage / ROM (GB)", rom_options, index=rom_options.index(512) if 512 in rom_options else 0)
    rom_type = st.selectbox("Storage Type", options["ROM_type"])
    gpu_brand = st.selectbox("GPU Brand", options["GPU_brand"])

with col2:
    os_choice = st.selectbox("Operating System", options["OS"])
    display_size = st.slider(
        "Display Size (inches)",
        min_value=float(num_ranges["display_size"]["min"]),
        max_value=float(num_ranges["display_size"]["max"]),
        value=float(num_ranges["display_size"]["default"]),
        step=0.1,
    )
    resolution_width = st.selectbox(
        "Resolution Width (px)", [1080, 1366, 1920, 2560, 2880, 3200, 3840],
        index=2,
    )
    resolution_height = st.selectbox(
        "Resolution Height (px)", [768, 900, 1080, 1440, 1600, 1800, 2160],
        index=2,
    )
    spec_rating = st.slider(
        "Spec Rating",
        min_value=float(num_ranges["spec_rating"]["min"]),
        max_value=float(num_ranges["spec_rating"]["max"]),
        value=float(num_ranges["spec_rating"]["default"]),
    )
    warranty = st.selectbox(
        "Warranty (years)",
        sorted(set(int(v) for v in [0, 1, 2, 3])),
        index=1,
    )

st.divider()
predict_clicked = st.button("🔮 Predict Price", use_container_width=True, type="primary")


# Build features exactly the same way ml.ipynb did, then predict
def build_input_row():
    total_pixels = resolution_width * resolution_height
    ppi = np.sqrt(resolution_width ** 2 + resolution_height ** 2) / display_size
    display_area = display_size ** 2

    row = {
        "brand": brand,
        "Ram_type": ram_type,
        "ROM_type": rom_type,
        "OS": os_choice,
        "processor_brand": processor_brand,
        "GPU_brand": gpu_brand,
        "spec_rating": spec_rating,
        "display_size": display_size,
        "resolution_width": resolution_width,
        "resolution_height": resolution_height,
        "warranty": warranty,
        "Ram": ram,
        "ROM": rom,
        "Total_Pixels": total_pixels,
        "PPI": ppi,
        "Display_Area": display_area,
    }
    return pd.DataFrame([row])


if predict_clicked:
    input_df = build_input_row()

    cat_encoded = encoder.transform(input_df[cat_cols])
    num_scaled = scaler.transform(input_df[num_cols])
    X_input = np.hstack([num_scaled, cat_encoded])

    # Polynomial Regression needs its features expanded the same way as training
    if meta.get("uses_polynomial"):
        poly = PolynomialFeatures(degree=meta["poly_degree"], include_bias=False)
        # NOTE: PolynomialFeatures must be fit on the same numeric columns
        # used at training time; since we only saved the fitted model here,
        # we rebuild the same transform on the scaled numeric input.
        X_input = poly.fit_transform(num_scaled)

    predicted_price = model.predict(X_input)[0]

    st.success("Prediction complete!")
    st.metric(label="💰 Estimated Price", value=f"रु {predicted_price:,.0f}")
    st.caption(
        "This is an estimate based on historical listing prices for laptops "
        "with similar specs — actual prices may vary by retailer and region."
    )