# pages/2_Admin_Dashboard.py
import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import database module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db

st.set_page_config(page_title="Admin Dashboard", layout="wide")

#  Authentication Check 
if not st.session_state.get('admin_logged_in', False):
    st.error("Access denied. Please sign in as an administrator on the main page.")
    st.stop()

# Admin Page Content
st.title("Admin Dashboard")
st.write("View all candidate profiles saved to the database.")

records = db.view_all_candidates()

if not records:
    st.warning("No candidate submissions found in the database yet.")
else:
    data_for_df = [dict(row) for row in records]
    df = pd.DataFrame(data_for_df)
    column_order = [
        'id', 'full_name', 'email', 'phone', 'submission_time', 'years_experience',
        'desired_positions', 'location', 'tech_stack', 'sentiment_analysis', 'technical_answers'
    ]
    df_columns = [col for col in column_order if col in df.columns]
    df = df[df_columns]

    st.dataframe(df, use_container_width=True)

    if st.button("Refresh Data"):
        st.rerun()