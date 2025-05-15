import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Real Estate Analytics", layout="wide")

# Load data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Sidebar navigation
st.sidebar.title("📊 Navigation")
section = st.sidebar.radio("Select Section", [
    'Overview', 
    'Price per Sqft Geomap', 
    'Feature Word Cloud', 
    'Area vs Price',
    'BHK Distribution',
    'BHK Price Comparison',
    'Property Type Distribution'
])

st.title("🏡 Real Estate Data Analytics Dashboard")

# 1. Overview
if section == 'Overview':
    st.subheader("Dataset Preview")
    st.write(new_df.head())
    st.markdown(f"**Total Records:** {len(new_df)}")
    st.markdown(f"**Columns:** {', '.join(new_df.columns)}")

# 2. Price per Sqft Geomap
elif section == 'Price per Sqft Geomap':
    st.subheader("📍 Sector Price per Sqft Map")
    group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().dropna()
    
    fig = px.scatter_mapbox(group_df,
                            lat="latitude",
                            lon="longitude",
                            color="price_per_sqft",
                            size="built_up_area",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            zoom=10,
                            mapbox_style="open-street-map",
                            width=1100,
                            height=600,
                            hover_name=group_df.index)
    st.plotly_chart(fig)

# 3. Word Cloud
elif section == 'Feature Word Cloud':
    st.subheader("☁️ Word Cloud of Common Features")
    wordcloud = WordCloud(width=800, height=800, background_color='white',
                          stopwords=set(['s']), min_font_size=10).generate(feature_text)
    fig1, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig1)

# 4. Area vs Price Scatter
elif section == 'Area vs Price':
    st.subheader("📐 Area vs Price by Property Type")
    property_type = st.selectbox('Select Property Type:', ['flat', 'house'])

    filtered = new_df[new_df['property_type'] == property_type]
    fig2 = px.scatter(filtered, x='built_up_area', y='price', color='bedRoom',
                      title=f'{property_type.capitalize()} - Area vs Price',
                      labels={'built_up_area': 'Built-up Area (sqft)', 'price': 'Price'})
    st.plotly_chart(fig2)

# 5. BHK Distribution Pie
elif section == 'BHK Distribution':
    st.subheader("🏠 BHK Distribution by Sector")
    sectors = ['Overall'] + sorted(new_df['sector'].dropna().unique().tolist())
    selected_sector = st.selectbox('Choose Sector:', sectors)
    
    if selected_sector == 'Overall':
        df = new_df
    else:
        df = new_df[new_df['sector'] == selected_sector]

    fig3 = px.pie(df, names='bedRoom', title=f'BHK Distribution - {selected_sector}')
    st.plotly_chart(fig3)

# 6. BHK vs Price Boxplot
elif section == 'BHK Price Comparison':
    st.subheader("📦 BHK vs Price Comparison")
    temp_df = new_df[new_df['bedRoom'] <= 4]
    fig4 = px.box(temp_df, x='bedRoom', y='price', title='Price Distribution by Bedroom Count (BHK)',
                  labels={'bedRoom': 'Bedrooms', 'price': 'Price'})
    st.plotly_chart(fig4)

# 7. Property Type Distribution
elif section == 'Property Type Distribution':
    st.subheader("📊 Price Distribution by Property Type")
    fig5 = plt.figure(figsize=(10, 4))
    sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color='skyblue')
    sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House', kde=True, color='salmon')
    plt.legend()
    plt.title('Price Distribution: Flat vs House')
    st.pyplot(fig5)
