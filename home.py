import streamlit as st

st.set_page_config(page_title="🏘️ Smart Property Advisor", layout="centered")

# Title
st.title("🏘️ Smart Property Advisor")
st.markdown("### 🔍 Personalized Recommendations & Accurate Price Predictions")

# Project Overview
st.subheader("📌 Project Overview")
st.markdown("""
**Smart Property Advisor** is an end-to-end real estate analytics application built using **Streamlit**.  
It leverages **machine learning** and **data visualization** to empower users—buyers, renters, and investors—with smarter, data-backed decisions.

---

### 🎯 Objective
To create an intelligent tool that:
- ✅ Recommends similar properties based on features, configuration, and design
- ✅ Predicts accurate price ranges for residential properties
- ✅ Visualizes key property trends and location insights

---

### 🧠 Key Features
- 🏡 **Apartment Recommender**: Suggests top similar properties using a weighted cosine similarity score across features and textual data.
- 💰 **Price Estimator**: Predicts property prices using a trained regression model and displays a confidence range.
- 📊 **Visual Dashboard** *(optional)*: Interactive plots showing sector-wise pricing, area comparisons, and bedroom trends.

---

### 🔧 Tech Stack
- **Frontend**: Streamlit
- **Backend & ML**: Scikit-learn, Pandas, NumPy, Pickle
- **Visualization**: Plotly, Seaborn, WordCloud
- **Data**: Cleaned real estate dataset with attributes like sector, property type, BHK, area, amenities, etc.

---

### 🚀 Outcome
This tool transforms raw housing data into actionable insights. It blends real-world usability with robust data science, making property exploration efficient and insightful.

""")
