# app.py
import streamlit as st
from streamlit_extras.app_logo import add_logo

# Page Configuration
st.set_page_config(
    page_title="TalentHunt AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Look & Clickable Cards
st.markdown("""
    <style>
        /* Main Container Styling */
        .main {
            background-color: #0e1117;
        }
        
        /* Hero Section */
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #FAFAFA;
            text-align: center;
            margin-bottom: 3rem;
            font-weight: 300;
        }
        
        /* Button Styling to look like Cards */
        .stButton > button {
            width: 100%;
            height: auto;
            min-height: 250px;
            background-color: #262730;
            border: 1px solid #41444C;
            border-radius: 20px;
            color: #FFFFFF;
            text-align: center;
            padding: 2rem;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            white-space: pre-wrap; /* Allow newlines */
            line-height: 1.5;
        }
        
        .stButton > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            border-color: #FF4B4B;
            background-color: #262730; /* Keep background same */
            color: #FFFFFF;
        }
        
        .stButton > button:active {
            background-color: #1E1E24;
            border-color: #FF4B4B;
        }
        
        /* Text Styling inside buttons */
        .stButton > button p {
            font-size: 1rem;
        }

        /* Footer */
        .footer {
            position: fixed; 
            bottom: 20px; 
            width: 100%; 
            text-align: center; 
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero-title">TalentHunt AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">The Future of Autonomous Recruitment</div>', unsafe_allow_html=True)

# Spacing
st.write("")
st.write("")

# Role Selection Cards (Implemented as Big Buttons)
col1, col2, col3, col4 = st.columns([1, 4, 4, 1])

with col2:
    # Candidate Button
    candidate_text = "🚀\n\nFor Candidates\n\nReady to find your dream job? Upload your resume, take our AI screening test, and get instant feedback."
    if st.button(candidate_text, key="candidate_card", use_container_width=True):
        st.switch_page("pages/01_Candidate_Portal.py")

with col3:
    # Recruiter Button
    recruiter_text = "👔\n\nFor Recruiters\n\nStreamline your hiring process. View ranked profiles, analyze interview transcripts, and find top talent."
    if st.button(recruiter_text, key="recruiter_card", use_container_width=True):
        st.switch_page("pages/02_Recruiter_Dashboard.py")

# Footer
st.markdown("""
    <div class="footer">
        Powered by <b>TalentHunt AI</b> &bull; Built with Streamlit & Ollama
    </div>
""", unsafe_allow_html=True)