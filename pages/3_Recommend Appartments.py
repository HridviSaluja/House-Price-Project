import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="🏙️ Smart Apartment Recommender", layout="centered")

# Load data
location_df = pickle.load(open('datasets/location_df.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# Combine similarity matrices with custom weights
combined_sim = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

# Recommender function
def recommend_properties(property_name, top_n=5):
    idx = location_df.index.get_loc(property_name)
    sim_scores = list(enumerate(combined_sim[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [round(i[1], 3) for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        '🏘️ Property Name': top_properties,
        '📊 Similarity Score': top_scores
    })

    return recommendations_df

# --- Streamlit UI ---
st.title("🏡 Smart Apartment Recommender")

st.markdown("Get apartment recommendations based on similar features like amenities, size, and category.")

# Select apartment
selected_apartment = st.selectbox("🔍 Choose a reference apartment:", sorted(location_df.index.to_list()))

# Recommend button
if st.button("🎯 Recommend"):
    st.info("Finding similar apartments...")
    df_recommend = recommend_properties(selected_apartment)

    if df_recommend.empty:
        st.warning("No similar properties found.")
    else:
        st.success(f"Top recommendations similar to **{selected_apartment}**:")
        st.dataframe(df_recommend.style.highlight_max(axis=0, subset=["📊 Similarity Score"]))
