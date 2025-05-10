# modules/clustering.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def perform_clustering(df, n_clusters=4):
    """
    Performs K-Means clustering on selected features.
    Returns the dataframe with a new 'Cluster' column.
    """
    # Features for clustering
    features = [
        'App_Usage_Time',
        'Screen_On_Time',
        'Battery_Drain',
        'Data_Usage',
        'Battery_Efficiency',
        'Usage_Per_App'
    ]

    X = df[features].copy()

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    clusters = kmeans.fit_predict(X_scaled)
    df['Cluster'] = clusters

    return df, kmeans


def reduce_dimensions(df, features):
    """
    Reduces dimensions of the feature space for 2D visualization.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)

    df_pca = pd.DataFrame(components, columns=['PC1', 'PC2'])
    df_pca['Cluster'] = df['Cluster'].values
    return df_pca


def plot_clusters(df_pca):
    """
    Plots PCA-reduced 2D clusters.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Cluster', palette='Set2', s=70)
    plt.title('User Clusters (PCA Reduced)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Cluster')
    plt.tight_layout()
    st.pyplot(plt)
