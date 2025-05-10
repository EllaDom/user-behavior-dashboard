# app.py

import streamlit as st
import pandas as pd
from modules.preprocessing import preprocess_data
from modules.clustering import perform_clustering, reduce_dimensions, plot_clusters

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/user_behavior_dataset.csv")
    return df

st.set_page_config(page_title="User Behavior Dashboard", layout="wide")
st.title("📊 User Behavior Analytics Dashboard")

# Load & preprocess data
df = load_data()
df_processed, label_encoders = preprocess_data(df)

# Sidebar controls
st.sidebar.header("🔧 Configuration")
n_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=4)

# Perform clustering
df_clustered, kmeans_model = perform_clustering(df_processed, n_clusters=n_clusters)

# PCA for plotting
features_to_reduce = [
    'App_Usage_Time', 'Screen_On_Time', 'Battery_Drain',
    'Data_Usage', 'Battery_Efficiency', 'Usage_Per_App'
]
df_pca = reduce_dimensions(df_clustered, features_to_reduce)

# Main content area
st.subheader("📌 Cluster Overview")

# Cluster stats table
st.dataframe(
    df_clustered.groupby('Cluster')[features_to_reduce].mean().round(2),
    use_container_width=True
)

# Cluster plot
st.subheader("🧩 Cluster Visualization (PCA)")
plot_clusters(df_pca)

# Optional: Show raw data
with st.expander("🔍 Show Raw Processed Data"):
    st.dataframe(df_clustered.head(20))
