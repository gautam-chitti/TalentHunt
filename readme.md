# TalentHunt AI 

**TalentHunt AI** is an Autonomous AI Hiring System designed to streamline the recruitment process. It leverages **RAG (Retrieval-Augmented Generation)** and **Large Language Models (LLMs)** to screen resumes, conduct initial technical interviews, and rank candidates based on semantic fit.

![System Architecture](images/architecture.png)

## Key Features

-   **Autonomous Screening:** Parses PDF resumes and calculates a **Semantic Match Score** against the Job Description using Vector Embeddings.
-   **AI Interviewer:** Conducts dynamic, chat-based technical interviews using **Mistral 7B**. Questions are tailored to the candidate's resume gaps.
-   **Recruiter Dashboard:** A secure, password-protected dashboard for recruiters to view ranked candidates, interview transcripts, and AI summaries.
-   **Premium UI/UX:** A modern, dark-themed interface with role-based navigation.

## Application Screenshots

### Landing Page
The entry point for both Candidates and Recruiters.
![Landing Page](images/landing.png)

### Candidate Journey
1.  **Registration:** Candidates enter their details.
    ![Registration](images/RegisterCandidate.png)
2.  **Screening:** Resume is analyzed against the JD.
    ![Screening Result](images/ProceedTotest.png)
3.  **AI Interview:** Dynamic technical interview based on the resume.
    ![AI Interview](images/chat.png)
4.  **Completion:** Final feedback and score.
    ![Test Done](images/Testdone.png)

### Recruiter Dashboard
View ranked candidates and detailed insights.
![Recruiter Dashboard](images/RecruiterDash.png)

## 🛠️ Tech Stack

-   **Frontend:** Streamlit
-   **LLM:** Ollama (Mistral 7B Instruct)
-   **Embeddings:** Nomic Embed Text
-   **Vector Store:** ChromaDB
-   **Orchestration:** LangChain
-   **Database:** SQLite

## Getting Started

### Prerequisites

1.  **Python 3.10+**
2.  **Ollama** installed and running locally.
    -   Download from [ollama.com](https://ollama.com).
    -   Pull the required models:
        ```bash
        ollama pull mistral:7b-instruct
        ollama pull nomic-embed-text
        ```

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gautam-chitti/TalentHunt
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

## Project Report
A detailed project report (`project_report.tex`) is included in the root directory. You can compile it using any LaTeX editor to generate a PDF documentation of the project.

---
