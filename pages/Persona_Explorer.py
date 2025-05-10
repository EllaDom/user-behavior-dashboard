# pages/3_👤_Persona_Explorer.py

import streamlit as st
import pandas as pd
from modules.preprocessing import preprocess_data
from modules.persona import get_filtered_persona, format_persona_card

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("data/user_behavior_dataset.csv")
    df_processed, _ = preprocess_data(df)
    return df_processed

df = load_data()

st.title("👤 Persona Explorer")

# Sidebar filters
st.sidebar.header("🔍 Select Persona Traits")
os = st.sidebar.selectbox("Operating System", [None] + sorted(df['Operating_System'].unique().tolist()))
gender = st.sidebar.selectbox("Gender", [None] + sorted(df['Gender'].unique().tolist()))
behavior_class = st.sidebar.selectbox("User Behavior Class", [None] + sorted(df['User_Behavior_Class'].unique().tolist()))
age_group = st.sidebar.selectbox("Age Group", [None] + sorted(df['Age_Group'].dropna().unique().tolist()))

# Retrieve persona
persona = get_filtered_persona(df, os=os, gender=gender, behavior_class=behavior_class, age_group=age_group)
persona_card = format_persona_card(persona)

# Display persona
st.markdown(persona_card)

# Optional: Show full raw data of this persona
if persona is not None:
    with st.expander("📋 Show Full Data Record"):
        st.dataframe(pd.DataFrame([persona]))
