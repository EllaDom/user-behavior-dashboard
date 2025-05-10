# modules/retention.py

import pandas as pd


def flag_churn_risk(df, usage_threshold=150, screen_time_threshold=3.0, data_threshold=500):
    """
    Flags users who fall below specified thresholds as likely to churn.
    Returns a modified DataFrame with 'Likely_Churn' column.
    """
    df = df.copy()
    df['Likely_Churn'] = ((df['App_Usage_Time'] < usage_threshold) &
                          (df['Screen_On_Time'] < screen_time_threshold) &
                          (df['Data_Usage'] < data_threshold)).astype(int)
    return df


def get_churn_summary(df):
    """
    Returns a summary of retained vs likely to churn users.
    """
    churn_counts = df['Likely_Churn'].value_counts().rename(index={0: 'Retained', 1: 'Likely to Churn'})
    return churn_counts


def get_high_risk_users(df, limit=10):
    """
    Returns a sample of users who are flagged as high churn risk.
    """
    return df[df['Likely_Churn'] == 1].head(limit)
