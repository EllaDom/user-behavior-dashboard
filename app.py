# app.py

import streamlit as st

st.set_page_config(page_title="User Behavior Dashboard", layout="wide")

st.title("📱 User Behavior Analytics Dashboard")

st.markdown("""
Welcome to the interactive dashboard for analyzing and visualizing app user behavior.

Use the tabs on the left to explore:
- **📊 EDA**: Core behavioral insights and visual distributions
- **🧩 Clustering**: K-Means segmentation of users
- **👤 Persona Explorer**: Filter and view real user profiles
- **🔄 Retention Analysis**: Simulated churn detection
- **🎯 Recommendations**: Data-driven improvement strategies

""")
