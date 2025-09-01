# pages/1_Take_Screening_Test.py
import streamlit as st
import json
import sys
import os

# Add the parent directory to the path to import the database module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
from typing import List

# The rest of the chatbot code is identical to the last version you had.
# Copy the entire content of the previous corrected app.py here,
# starting from the "try...import ollama" block.

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Page Config
st.set_page_config(page_title="Screening Test", page_icon="📝")
db.init_db() # Ensure database and table exist

# Constants 
REQUIRED_FIELDS = [
    ("full_name", "Full Name"),
    ("email", "Email Address"),
    ("phone", "Phone Number"),
    ("years_experience", "Years of Experience"),
    ("desired_positions", "Desired Position(s)"),
    ("location", "Current Location"),
    ("tech_stack", "Tech Stack (e.g., Python, React, SQL)"),
]
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye"}

# Session State Setup 
def reset_session():
    st.session_state.stage = "gathering_info"
    st.session_state.current_field_index = 0
    st.session_state.candidate_data = {}
    st.session_state.conversation = [("assistant", "Hello! I'm the TalentHunt Hiring Assistant. Let's start with your full name.")]

if 'stage' not in st.session_state:
    reset_session()

#  Helper Functions 
def append_message(role: str, text: str):
    st.session_state.conversation.append((role, text))

def generate_questions(tech_stack: str, n: int = 4) -> List[str]:
    if not OLLAMA_AVAILABLE:
        st.warning("Ollama not found. Using fallback question generator.")
        return [f"Describe a project where you used {tech.strip()}." for tech in tech_stack.split(',')[:n]]
    prompt = f"""
    Generate exactly {n} concise and relevant technical questions for a candidate with this tech stack: {tech_stack}.
    IMPORTANT: Your response must begin immediately with "1." and contain nothing but the numbered list of questions. Do not add any introductory text.
    """
    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        content = response['message']['content']
        questions = []
        for line in content.strip().split('\n'):
            clean_line = line.strip()
            if clean_line and clean_line[0].isdigit() and '.' in clean_line:
                question_text = clean_line.split('.', 1)[-1].strip()
                if question_text:
                    questions.append(question_text)
        if not questions:
            raise ValueError("LLM response did not contain a valid numbered list.")
        return questions[:n]
    except Exception as e:
        st.error(f"LLM generation failed: {e}")
        return [f"How do you handle version control in a project involving {tech_stack}?", "Describe a complex bug you've debugged."]

def analyze_sentiment_with_llm(answers: dict) -> str:
    if not OLLAMA_AVAILABLE:
        return "Sentiment analysis unavailable."
    answers_text = json.dumps(answers, indent=2)
    prompt = f"""As a senior hiring manager, analyze the following technical answers for sentiment and confidence.
    Candidate's Answers:
    {answers_text}
    ---
    Provide a brief, one-sentence summary (e.g., "Candidate appears confident and knowledgeable," or "Candidate seems hesitant but provides logical answers.")."""
    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return response['message']['content'].strip()
    except Exception:
        return "Could not perform sentiment analysis."

# UI 
st.title("AI Screening Test")

for role, text in st.session_state.conversation:
    with st.chat_message(role):
        st.markdown(text)

if st.session_state.stage == "finished":
    st.success("Your screening is complete. Thank you for your time!")
    if st.button("Take Another Test"):
        reset_session()
        st.rerun()
    st.stop()

user_input = st.chat_input("Type your answer here...")

if user_input:
    user_input = user_input.strip()
    append_message("user", user_input)

    if user_input.lower() in EXIT_KEYWORDS:
        append_message("assistant", "You've chosen to end the session. Goodbye!")
        st.session_state.stage = "finished"
    
    elif st.session_state.stage == "gathering_info":
        key, _ = REQUIRED_FIELDS[st.session_state.current_field_index]
        st.session_state.candidate_data[key] = user_input
        st.session_state.current_field_index += 1

        if st.session_state.current_field_index >= len(REQUIRED_FIELDS):
            append_message("assistant", "Thank you. I have all your profile information. Now, I'll generate a few technical questions based on your stack.")
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(st.session_state.candidate_data["tech_stack"])
            st.session_state.candidate_data["technical_answers"] = {"questions": st.session_state.questions, "answers": []}
            st.session_state.stage = "answering_questions"
            first_question = st.session_state.questions[0]
            append_message("assistant", f"**Question 1/{len(st.session_state.questions)}:**\n\n{first_question}")
        else:
            _, next_label = REQUIRED_FIELDS[st.session_state.current_field_index]
            append_message("assistant", f"Got it. Next, what is your **{next_label}**?")

    elif st.session_state.stage == "answering_questions":
        answers_list = st.session_state.candidate_data["technical_answers"]["answers"]
        answers_list.append(user_input)
        
        if len(answers_list) >= len(st.session_state.questions):
            append_message("assistant", "Thank you for your answers. Please wait a moment while I finalize your profile.")
            with st.spinner("Analyzing answers and saving profile..."):
                sentiment = analyze_sentiment_with_llm(st.session_state.candidate_data["technical_answers"])
                st.session_state.candidate_data["sentiment_analysis"] = sentiment
                record_id = db.save_candidate(st.session_state.candidate_data)
            final_message = f"**Thank you! Your screening is complete.**\n\n- **Sentiment Analysis:** {sentiment}\n- Your profile has been saved, Our team will contact you soon."
            append_message("assistant", final_message)
            st.session_state.stage = "finished"
        else:
            next_q_index = len(answers_list)
            next_question = st.session_state.questions[next_q_index]
            append_message("assistant", f"**Question {next_q_index + 1}/{len(st.session_state.questions)}:**\n\n{next_question}")

    st.rerun()