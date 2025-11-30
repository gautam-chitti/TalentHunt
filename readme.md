# **TalentHunt AI Hiring Assistant**

## **1\. Project Overview**

This project is an intelligent Hiring Assistant chatbot developed for the fictional recruitment agency "TalentScout". The application serves as a comprehensive initial screening tool that interacts with candidates to gather essential profile information, conducts a preliminary technical assessment using a Large Language Model (LLM), and securely stores the data for administrator review.

The system features a dual-interface design: a conversational AI for candidates and a secure dashboard for administrators to view and manage submissions. This project was built to satisfy the requirements of the PG-AGI AI/ML Intern Assignment.

## **2\. Architecture and Features**

The application is a multi-page Streamlit web app with role-based access control.

### **Key Features:**

- **User Portal:** A main landing page that directs users to either the candidate screening test or an administrator login form.
- **Candidate Screening Chatbot:**
  - A conversational interface that guides candidates through a structured information-gathering process.
  - Dynamically generates tailored technical questions based on the candidate's declared tech stack using a local LLM (Ollama with Llama 3).
  - Collects answers and concludes the session gracefully.
- **Secure Admin Dashboard:**
  - A password-protected page accessible only to administrators.
  - Displays all candidate submissions in a clean, tabular format.
  - **Hardcoded Credentials:** For this assignment, administrator access is granted using the following hardcoded credentials:
    - **Email:** admin@talenthunt.com
    - **Password:** admin123
- **Persistent Data Storage:**
  - All candidate data is stored in a local SQLite database (candidates.db), ensuring data persistence between sessions.
- **AI-Powered Sentiment Analysis:**
  - As a bonus feature, the application uses the LLM to perform a brief sentiment and confidence analysis on the candidate's technical answers, providing recruiters with an at-a-glance impression.

### **File Structure:**

talent-scout-chatbot/  
|-- app.py \# Main landing/login page  
|-- database.py \# SQLite database logic  
|-- requirements.txt \# Project dependencies  
\`-- pages/  
 |-- 1_Take_Screening_Test.py \# Chatbot UI and logic for candidates  
 \`-- 2_Admin_Dashboard.py \# Data viewer for the admin

## **3\. Technical Details**

- **Programming Language:** Python
- **Frontend Framework:** Streamlit
- **Large Language Model:** Llama 3 (via Ollama)
- **Database:** SQLite

## Getting Started

### Prerequisites

1.  **Python 3.10+**
2.  **Ollama** installed and running locally.
    - Download from [ollama.com](https://ollama.com).
    - Pull the required models:
      ```bash
      ollama pull mistral:7b-instruct
      ollama pull nomic-embed-text
      ```

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd TalentHunt
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

2.  **Access the App:**
    Open your browser at `http://localhost:8501`.

## User Guide

### For Candidates

1.  **Landing Page:** Click **"Start Your Journey"**.
2.  **Register:** Enter your details (Name, Email, Skills).
    ![Registration](images/RegisterCandidate.png)
3.  **Upload Resume:** Select a Role and Upload your PDF Resume.
    ![Resume Upload](images/ProceedTotest.png)
4.  **AI Interview:** If your resume matches (> 40%), you will proceed to the interview.
    ![AI Interview](images/chat.png)
5.  **Feedback:** Receive your **Match Score** immediately.
    ![Completion](images/Testdone.png)

### For Recruiters

1.  **Login:** Access the dashboard with credentials (`admin@talenthunt.com` / `admin123`).
2.  **Dashboard:** View the **Leaderboard** of candidates ranked by score.
    ![Recruiter Dashboard](images/RecruiterDash.png)
3.  **Deep Dive:** Expand any candidate to see their **Resume Summary**, **Interview Transcript**, and **Contact Details**.
