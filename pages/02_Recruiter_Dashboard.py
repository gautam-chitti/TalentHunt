# pages/02_Recruiter_Dashboard.py
import streamlit as st
import pandas as pd
import json
import sys
import os

# Add parent directory to path to import database module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db

st.set_page_config(page_title="Recruiter Dashboard", layout="wide", page_icon="👔")

# Hide Sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

#  Authentication Check 
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<h2 style='text-align: center;'>Recruiter Login</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if email == "admin@talenthunt.com" and password == "admin123":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    st.stop()

# Admin Page Content
st.title("Recruiter Dashboard")
st.write("View all candidate profiles saved to the database.")

records = db.view_all_candidates()

if not records:
    st.warning("No candidate submissions found in the database yet.")
else:
    data_for_df = [dict(row) for row in records]
    df = pd.DataFrame(data_for_df)
    
    # Ensure new columns exist (handle old DB records if any)
    if 'match_score' not in df.columns:
        df['match_score'] = 0.0
    
    # Sort by Match Score
    df = df.sort_values(by='match_score', ascending=False)
    
    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates", len(df))
    col2.metric("Avg Match Score", f"{df['match_score'].mean():.2f}")
    col3.metric("Top Candidate Score", f"{df['match_score'].max():.2f}")
    
    st.divider()
    
    # Detailed View
    st.subheader("Candidate Rankings")
    
    for index, row in df.iterrows():
        with st.expander(f"#{index+1} | {row['full_name']} | Score: {row['match_score']:.2f}"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Email:** {row['email']}")
                st.write(f"**Phone:** {row['phone']}")
                st.write(f"**Experience:** {row['years_experience']}")
                st.write(f"**Tech Stack:** {row['tech_stack']}")
                st.write(f"**Sentiment:** {row['sentiment_analysis']}")
            with c2:
                st.write("**Resume Summary:**")
                st.caption(row.get('resume_text', '')[:500] + "...")
            
            st.divider()
            st.write("**Interview Transcript:**")
            transcript = row.get('interview_transcript')
            if transcript:
                try:
                    transcript_json = json.loads(transcript)
                    for msg in transcript_json:
                        role_icon = "🤖" if msg['role'] == "assistant" else "👤"
                        st.write(f"{role_icon} **{msg['role'].title()}:** {msg['content']}")
                except:
                    st.write("No transcript available or invalid format.")
            else:
                st.write("No interview conducted.")

    if st.button("Refresh Data"):
        st.rerun()
        
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.switch_page("app.py")
