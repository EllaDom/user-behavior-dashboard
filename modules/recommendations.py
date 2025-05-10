# modules/recommendations.py

def generate_recommendations(df_filtered, behavior_class=None):
    """
    Generates a list of recommendation strings based on segment behavior.
    """
    recs = []

    avg_usage = df_filtered['App_Usage_Time'].mean()
    avg_drain = df_filtered['Battery_Drain'].mean()
    avg_data = df_filtered['Data_Usage'].mean()

    if avg_usage < 200:
        recs.append("🔔 Send re-engagement notifications during peak hours.")
    else:
        recs.append("💎 Offer loyalty rewards to highly engaged users.")

    if avg_drain > 1500:
        recs.append("🔋 Optimize app performance for high-drain devices.")

    if avg_data > 1000:
        recs.append("📶 Implement data-saving modes for power users.")

    if behavior_class and behavior_class <= 2:
        recs.append("🎓 Re-show onboarding tutorials to low engagement users.")

    if avg_usage > 300 and avg_data < 500:
        recs.append("📈 Encourage use of richer in-app content or features.")

    return recs