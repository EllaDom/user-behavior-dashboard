# modules/preprocessing.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


def preprocess_data(df):
    """
    Cleans and enriches the raw user behavior dataset.
    """
    df = df.copy()

    # --- Handle missing values if any ---
    df.dropna(inplace=True)

    # --- Feature Engineering ---
    df['Battery_Efficiency'] = df['App_Usage_Time'] / df['Battery_Drain']
    df['Usage_Per_App'] = df['App_Usage_Time'] / df['Number_of_Apps_Installed']
    
    # Bin Age into groups
    df['Age_Group'] = pd.cut(
        df['Age'],
        bins=[0, 25, 35, 45, 60, 100],
        labels=['18-25', '26-35', '36-45', '46-60', '60+']
    )

    # Create Heavy User flag
    df['Heavy_User'] = ((df['App_Usage_Time'] > 300) & (df['Data_Usage'] > 1000)).astype(int)

    # --- Encode categorical columns ---
    label_encoders = {}
    cat_cols = ['Gender', 'Operating_System', 'Device_Model', 'Age_Group']
    for col in cat_cols:
        le = LabelEncoder()
        df[col + '_Encoded'] = le.fit_transform(df[col])
        label_encoders[col] = le

    return df, label_encoders


def get_features_for_modeling(df):
    """
    Returns a DataFrame with only the selected numerical features for modeling/clustering.
    """
    features = [
        'App_Usage_Time',
        'Screen_On_Time',
        'Battery_Drain',
        'Number_of_Apps_Installed',
        'Data_Usage',
        'Battery_Efficiency',
        'Usage_Per_App',
        'Gender_Encoded',
        'Operating_System_Encoded',
        'Age_Group_Encoded'
    ]
    return df[features].dropna()
