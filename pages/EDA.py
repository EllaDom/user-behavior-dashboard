# pages/1_📊_EDA.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from modules.preprocessing import preprocess_data

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("data/user_behavior_dataset.csv")
    df_processed, _ = preprocess_data(df)
    return df_processed

df = load_data()

st.title("📊 Exploratory Data Analysis")

st.markdown("""
This page provides key visual insights about user behavior across various dimensions like usage time, battery drain, age, and more.
""")

# Filter options
st.sidebar.header("🔍 Filters")
os = st.sidebar.selectbox("Operating System", ["All"] + sorted(df['Operating_System'].unique().tolist()))
gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df['Gender'].unique().tolist()))

if os != "All":
    df = df[df['Operating_System'] == os]
if gender != "All":
    df = df[df['Gender'] == gender]

# 1. Correlation heatmap
st.subheader("📈 Correlation Heatmap")
correlation_features = df.drop(columns=["User_ID"], errors="ignore").select_dtypes(include='number')
corr_matrix = correlation_features.corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, cbar=True, annot_kws={"size": 7})
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
st.pyplot(fig)
app_usage_corrs = corr_matrix['App_Usage_Time'].drop('App_Usage_Time')
strongest_corr = app_usage_corrs.abs().idxmax()
st.caption(f"📌 App Usage Time is most strongly correlated with **{strongest_corr.replace('_', ' ')}** (corr = {app_usage_corrs[strongest_corr]:.2f}).")

# 2. Distribution of App Usage Time
st.subheader("📉 App Usage Time Distribution")
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.histplot(df['App_Usage_Time'], kde=True, ax=ax2, color='skyblue')
ax2.set_xlabel("App Usage Time (minutes)")
st.pyplot(fig2)
skew = df['App_Usage_Time'].skew()
skew_type = "right-skewed" if skew > 0 else ("left-skewed" if skew < 0 else "symmetric")
st.caption(f"App Usage Time distribution is {skew_type} (skew = {skew:.2f}).")

# 3. Boxplot: Battery Drain by OS
st.subheader("🔋 Battery Drain by OS")
fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.boxplot(x="Operating_System", y="Battery_Drain", data=df, ax=ax3)
st.pyplot(fig3)
mean_drain = df.groupby('Operating_System')['Battery_Drain'].mean().idxmax()
st.caption(f"On average, {mean_drain} devices have the highest battery drain.")

# 4. Barplot: Average Data Usage by Age Group
st.subheader("🌐 Avg. Data Usage by Age Group")
fig4, ax4 = plt.subplots(figsize=(6, 4))
sns.barplot(x="Age_Group", y="Data_Usage", data=df, estimator='mean', ci=None, ax=ax4)
st.pyplot(fig4)
max_group = df.groupby('Age_Group')['Data_Usage'].mean().idxmax()
st.caption(f"The {max_group} group consumes the most data on average.")

# 5. Stripplot: User Behavior Class vs App Usage
st.subheader("🧭 Behavior Class vs App Usage Time")
fig5, ax5 = plt.subplots(figsize=(6, 4))
sns.stripplot(x="User_Behavior_Class", y="App_Usage_Time", data=df, jitter=True, alpha=0.6, ax=ax5)
st.pyplot(fig5)
avg_by_class = df.groupby('User_Behavior_Class')['App_Usage_Time'].mean().round(1).to_dict()
st.caption("App Usage Time increases with behavior class: " + ", ".join([f"Class {k}: {v} min" for k, v in avg_by_class.items()]))

# 6. Lineplot: Screen On Time vs Age
st.subheader("📺 Screen On Time vs Age")
fig6, ax6 = plt.subplots(figsize=(6, 4))
sns.lineplot(x="Age", y="Screen_On_Time", data=df, ax=ax6)
st.pyplot(fig6)
correlation = df['Age'].corr(df['Screen_On_Time'])
st.caption(f"Screen On Time shows a correlation of {correlation:.2f} with Age.")

# 7. Countplot: Number of Users by Gender
st.subheader("👥 User Count by Gender")
fig7, ax7 = plt.subplots(figsize=(6, 4))
sns.countplot(x="Gender", data=df, ax=ax7)
st.pyplot(fig7)
gender_counts = df['Gender'].value_counts().to_dict()
st.caption("User count by gender: " + ", ".join([f"{k}: {v}" for k, v in gender_counts.items()]))

# 8. Boxplot: Data Usage by Device Model
st.subheader("📱 Data Usage by Device Model")
fig8, ax8 = plt.subplots(figsize=(6, 4))
sns.boxplot(x="Device_Model", y="Data_Usage", data=df, ax=ax8)
ax8.tick_params(axis='x', rotation=30)
st.pyplot(fig8)
max_device = df.groupby('Device_Model')['Data_Usage'].mean().idxmax()
st.caption(f"{max_device} users consume the most data on average.")

# 9. Violin Plot: App Usage Time by Age Group
st.subheader("🎻 App Usage Time by Age Group")
fig9, ax9 = plt.subplots(figsize=(6, 4))
sns.violinplot(x="Age_Group", y="App_Usage_Time", data=df, ax=ax9)
st.pyplot(fig9)
stds = df.groupby('Age_Group')['App_Usage_Time'].std().dropna()
most_varied = stds.idxmax()
st.caption(f"The {most_varied} age group has the widest variation in app usage.")

# 10. Pairplot (Sample)
st.subheader("🔀 Feature Pair Relationships (Sample View)")
sample_df = df[["App_Usage_Time", "Battery_Drain", "Data_Usage", "User_Behavior_Class"]].sample(100, random_state=42)
fig10 = sns.pairplot(sample_df, hue="User_Behavior_Class", palette="Set2")
st.pyplot(fig10)
st.caption("Color grouping highlights clustering tendencies by User Behavior Class.")
