# pages/01_Candidate_Portal.py
import streamlit as st
import json
import sys
import os

# Add the parent directory to the path to import the database module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
from rag_engine import rag_engine
from interview_agent import interview_agent
from job_descriptions import JOBS
from typing import List

MATCH_THRESHOLD = 0.4  # Lowered for demo purposes

# Check for Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Page Config
st.set_page_config(page_title="Candidate Portal", page_icon="🚀")
db.init_db()

# Hide Sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Session State Setup
def reset_session():
    st.session_state.stage = "registration" # Start with registration
    st.session_state.candidate_data = {}
    st.session_state.conversation = [] 
    st.session_state.resume_text = ""
    st.session_state.match_score = 0.0
    st.session_state.questions_queue = []
    st.session_state.current_question = ""
    st.session_state.question_count = 0
    st.session_state.max_questions = 5
    st.session_state.selected_role = list(JOBS.keys())[0]
    # Registration fields
    st.session_state.reg_name = ""
    st.session_state.reg_email = ""
    st.session_state.reg_phone = ""
    st.session_state.reg_exp = ""
    st.session_state.reg_loc = ""
    st.session_state.reg_tech = ""

if 'stage' not in st.session_state:
    reset_session()

# Helper Functions
def append_message(role: str, text: str):
    st.session_state.conversation.append({"role": role, "content": text})

# UI
st.title("AI Screening Test")

# Stage 0: Registration
if st.session_state.stage == "registration":
    st.subheader("Candidate Registration")
    st.info("Please fill in your details to proceed.")
    
    with st.form("registration_form"):
        st.session_state.reg_name = st.text_input("Full Name", value=st.session_state.reg_name)
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.reg_email = st.text_input("Email", value=st.session_state.reg_email)
            st.session_state.reg_phone = st.text_input("Phone Number", value=st.session_state.reg_phone)
        with col2:
            st.session_state.reg_exp = st.text_input("Years of Experience", value=st.session_state.reg_exp)
            st.session_state.reg_loc = st.text_input("Current Location", value=st.session_state.reg_loc)
        
        st.session_state.reg_tech = st.text_area("Key Skills / Tech Stack", value=st.session_state.reg_tech, placeholder="e.g., Python, React, AWS")
        
        submitted = st.form_submit_button("Next: Upload Resume")
        
        if submitted:
            if not st.session_state.reg_name or not st.session_state.reg_email:
                st.error("Name and Email are required.")
            else:
                st.session_state.stage = "resume_upload"
                st.rerun()

# Stage 1: Resume Upload
elif st.session_state.stage == "resume_upload":
    st.info(f"Welcome, {st.session_state.reg_name}. Please select a role and upload your Resume (PDF).")
    
    # Role Selection
    selected_role = st.selectbox("Select Role", list(JOBS.keys()), index=list(JOBS.keys()).index(st.session_state.selected_role))
    st.session_state.selected_role = selected_role
    
    # Display JD Preview
    with st.expander("View Job Description"):
        st.markdown(JOBS[selected_role])

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Analyzing your resume against the Job Description..."):
            # 1. Parse PDF
            resume_text = rag_engine.parse_pdf(uploaded_file)
            st.session_state.resume_text = resume_text
            
            # 2. Add JD to Store
            current_jd_text = JOBS[selected_role]
            rag_engine.add_jd_to_store(current_jd_text)
            
            # 3. Calculate Score
            score = rag_engine.calculate_match_score(resume_text, current_jd_text)
            st.session_state.match_score = score
            
            # 4. Decision
            if score >= MATCH_THRESHOLD:
                st.success(f"Resume Screened Successfully! Match Score: {score:.2f}")
                st.balloons()
                if st.button("Proceed to Interview"):
                    st.session_state.stage = "interview_start"
                    st.rerun()
            else:
                st.error(f"Resume Match Score: {score:.2f}. Unfortunately, your profile does not meet the minimum requirements.")
                if st.button("Try Again"):
                    st.session_state.stage = "registration" # Go back to start or just upload again?
                    st.rerun()

# Stage 2: Interview Initialization
elif st.session_state.stage == "interview_start":
    with st.spinner("AI Interviewer is preparing questions based on your profile..."):
        # Generate initial questions based on RAG analysis
        current_jd_text = JOBS[st.session_state.selected_role]
        initial_qs = interview_agent.generate_initial_questions(
            st.session_state.resume_text, 
            current_jd_text, 
            n=3
        )
        st.session_state.questions_queue = initial_qs
        
        # Start the conversation
        intro_msg = f"Hello {st.session_state.reg_name}! I've reviewed your resume. Let's dive into your experience. " + initial_qs[0]
        st.session_state.current_question = initial_qs[0]
        st.session_state.questions_queue.pop(0)
        append_message("assistant", intro_msg)
        
        st.session_state.stage = "interview_active"
        st.session_state.question_count = 1
        st.rerun()

# Stage 3: Active Interview
elif st.session_state.stage == "interview_active":
    # Display Chat History
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your answer here...")

    if user_input:
        user_input = user_input.strip()
        append_message("user", user_input)
        
        st.session_state.question_count += 1
        
        if st.session_state.question_count > st.session_state.max_questions:
            finish_msg = "Thank you for your detailed responses. We have everything we need. Our team will be in touch!"
            append_message("assistant", finish_msg)
            st.session_state.stage = "finished"
            
            # Save Data
            st.session_state.candidate_data = {
                "full_name": st.session_state.reg_name,
                "email": st.session_state.reg_email,
                "phone": st.session_state.reg_phone,
                "years_experience": st.session_state.reg_exp,
                "location": st.session_state.reg_loc,
                "tech_stack": st.session_state.reg_tech,
                "desired_positions": st.session_state.selected_role,
                "resume_text": st.session_state.resume_text,
                "match_score": st.session_state.match_score,
                "interview_transcript": [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.conversation
                ],
                "candidate_summary": "Interview Completed"
            }
            db.save_candidate(st.session_state.candidate_data)
            st.rerun()
            
        else:
            with st.spinner("Thinking..."):
                if st.session_state.questions_queue:
                    next_q = st.session_state.questions_queue.pop(0)
                else:
                    next_q = interview_agent.generate_followup_question(
                        st.session_state.conversation, 
                        user_input
                    )
                
                st.session_state.current_question = next_q
                append_message("assistant", next_q)
                st.rerun()

# Stage 4: Finished
elif st.session_state.stage == "finished":
    st.balloons()
    st.success("Interview Complete!")
    
    st.markdown(f"""
    ### Thank You, {st.session_state.reg_name}!
    
    Your application for **{st.session_state.selected_role}** has been submitted.
    
    **Your Profile Match Score:** {st.session_state.match_score * 100:.1f}%
    
    Our recruitment team will review your interview transcript and get back to you at **{st.session_state.reg_email}**.
    """)
    
    st.info("You may now close this tab.")
    
    if st.button("Return to Home"):
        reset_session()
        st.switch_page("app.py")
