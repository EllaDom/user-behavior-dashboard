# pages/4_🔄_Retention.py

import streamlit as st
import pandas as pd
from modules.preprocessing import preprocess_data

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("data/user_behavior_dataset.csv")
    df_processed, _ = preprocess_data(df)
    return df_processed

df = load_data()

st.title("🔄 Retention Analysis")

st.markdown("""
This page simulates retention likelihood based on app usage behavior.
Low usage, low screen-on time, and low data consumption are used as proxies for **churn risk**.
""")

# Sidebar adjustable thresholds
st.sidebar.header("🔧 Adjust Retention Criteria")
usage_threshold = st.sidebar.slider("Max App Usage Time (min)", 50, 500, 150)
screen_time_threshold = st.sidebar.slider("Max Screen On Time (hrs)", 1.0, 6.0, 3.0)
data_threshold = st.sidebar.slider("Max Data Usage (MB)", 100, 1500, 500)

# Apply churn logic with current thresholds
df['Likely_Churn'] = ((df['App_Usage_Time'] < usage_threshold) &
                      (df['Screen_On_Time'] < screen_time_threshold) &
                      (df['Data_Usage'] < data_threshold)).astype(int)

# Show churn stats
churn_counts = df['Likely_Churn'].value_counts().rename(index={0: 'Retained', 1: 'Likely to Churn'})
st.subheader("📊 Retention Overview")
st.bar_chart(churn_counts)

# Display high-risk users
st.subheader("⚠️ High Churn Risk Users")

if st.checkbox("Show full list of high-risk users"):
    st.dataframe(df[df['Likely_Churn'] == 1])
else:
    st.dataframe(df[df['Likely_Churn'] == 1].head(10))

st.info(f"🔄 {df['Likely_Churn'].sum()} users are currently flagged as likely to churn.")