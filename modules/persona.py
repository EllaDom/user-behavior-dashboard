# modules/persona.py

import pandas as pd
import numpy as np


def get_filtered_persona(df, os=None, gender=None, behavior_class=None, age_group=None):
    """
    Filters the DataFrame based on selected persona traits.
    Returns a single representative user's data.
    """
    df_filtered = df.copy()

    if os:
        df_filtered = df_filtered[df_filtered['Operating_System'] == os]
    if gender:
        df_filtered = df_filtered[df_filtered['Gender'] == gender]
    if behavior_class:
        df_filtered = df_filtered[df_filtered['User_Behavior_Class'] == behavior_class]
    if age_group:
        df_filtered = df_filtered[df_filtered['Age_Group'] == age_group]

    if df_filtered.empty:
        return None

    # Return a random representative user
    return df_filtered.sample(1).iloc[0]


def format_persona_card(persona):
    """
    Returns a markdown-formatted string describing the persona.
    """
    if persona is None:
        return "No user matches the selected filters."

    card = f"""
    ### 👤 Persona Summary

    **Device:** {persona['Device_Model']} ({persona['Operating_System']})  
    **Gender:** {persona['Gender']}  
    **Age Group:** {persona['Age_Group']}  
    **User Behavior Class:** {persona['User_Behavior_Class']}  
    **Heavy User:** {'Yes' if persona['Heavy_User'] else 'No'}

    ---

    ### 📊 Usage Insights

    - **App Usage Time:** {persona['App_Usage_Time']} mins/day  
    - **Screen On Time:** {persona['Screen_On_Time']} hrs/day  
    - **Data Usage:** {persona['Data_Usage']} MB/day  
    - **Battery Drain:** {persona['Battery_Drain']} mAh/day  
    - **Battery Efficiency:** {persona['Battery_Efficiency']:.2f} min/mAh  

    ---

    ### 🎯 Recommendation
    
    Optimize app experience for {'engagement retention' if persona['User_Behavior_Class'] <= 2 else 'power usage'},
    consider push notifications or performance optimizations on {persona['Device_Model']}.
    """
    return card
