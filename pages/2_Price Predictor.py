import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="🏠 Property Price Predictor", layout="centered")

# Load saved model and data
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Title
st.title("🏡 Property Price Estimator")
st.markdown("Enter the property details below to estimate the expected price (in **Cr**).")

# --- INPUT FORM ---
with st.form("input_form"):
    st.subheader("🔧 Property Details")

    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox('Property Type', ['flat', 'house'])
        sector = st.selectbox('Sector', sorted(df['sector'].unique()))
        bedroom = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique())))
        bathroom = st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique()))
        balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique()))

    with col2:
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique()))
        built_up_area = float(st.number_input('Built-Up Area (sqft)', min_value=100.0))
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique()))
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique()))
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique()))

    submit = st.form_submit_button("Predict Price 💰")

# --- PREDICTION ---
if submit:
    input_data = [[
        property_type, sector, bedroom, bathroom, balcony, property_age,
        built_up_area, servant_room, store_room, furnishing_type,
        luxury_category, floor_category
    ]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    input_df = pd.DataFrame(input_data, columns=columns)

    # Prediction and confidence range
    base_price = np.expm1(pipeline.predict(input_df))[0]
    low_price = base_price - 0.22
    high_price = base_price + 0.22

    # Display result
    st.success(f"💰 Estimated Property Price: **₹ {round(base_price, 2)} Cr**")
    st.markdown(f"📊 **Expected Range:** ₹ {round(low_price, 2)} Cr – ₹ {round(high_price, 2)} Cr")



