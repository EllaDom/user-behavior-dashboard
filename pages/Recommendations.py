# pages/5_🎯_Recommendations.py

import streamlit as st
import pandas as pd
from modules.preprocessing import preprocess_data
from modules.recommendations import generate_recommendations

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("data/user_behavior_dataset.csv")
    df_processed, _ = preprocess_data(df)
    return df_processed

df = load_data()

st.title("🎯 Recommendations Engine")

st.markdown("""
Get targeted improvement strategies based on user traits and behavior. Select criteria to generate insights.
""")

# Sidebar filters
st.sidebar.header("📌 Choose a Segment")
os = st.sidebar.selectbox("Operating System", [None] + sorted(df['Operating_System'].unique().tolist()))
gender = st.sidebar.selectbox("Gender", [None] + sorted(df['Gender'].unique().tolist()))
behavior_class = st.sidebar.selectbox("User Behavior Class", [None] + sorted(df['User_Behavior_Class'].unique().tolist()))
cluster = st.sidebar.selectbox("Cluster (if available)", [None] + sorted(df['Cluster'].unique().tolist() if 'Cluster' in df.columns else []))

# Filter data
df_filtered = df.copy()
if os:
    df_filtered = df_filtered[df_filtered['Operating_System'] == os]
if gender:
    df_filtered = df_filtered[df_filtered['Gender'] == gender]
if behavior_class:
    df_filtered = df_filtered[df_filtered['User_Behavior_Class'] == behavior_class]
if cluster is not None:
    df_filtered = df_filtered[df_filtered['Cluster'] == cluster]

# Show summary and recommendations
if df_filtered.empty:
    st.warning("No users match the selected filters.")
else:
    st.subheader("📊 Segment Summary")
    st.write(df_filtered.describe())

    st.subheader("🧠 Recommendations")
    recs = generate_recommendations(df_filtered, behavior_class)

    for r in recs:
        st.markdown(f"- {r}")
