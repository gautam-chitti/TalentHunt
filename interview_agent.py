import ollama
import json
from typing import List, Dict

class InterviewAgent:
    def __init__(self, model_name="mistral:7b-instruct"):
        self.model_name = model_name
        self.system_prompt = """
        You are an expert Technical Interviewer. Your goal is to assess the candidate's fit for the role based on their Resume and the Job Description.
        
        Guidelines:
        1. Ask one question at a time.
        2. Focus on gaps identified in the resume vs JD.
        3. Dig deeper if the candidate's answer is vague.
        4. Be professional but conversational.
        5. After 4-5 questions, conclude the interview.
        """

    def generate_initial_questions(self, resume_text: str, jd_text: str, n: int = 3) -> List[str]:
        """Generates a list of initial questions based on the Resume and JD analysis."""
        prompt = f"""
        Analyze the following Resume and Job Description. Identify key gaps or areas that need verification.
        
        Job Description:
        {jd_text[:2000]}
        
        Resume:
        {resume_text[:2000]}
        
        Generate exactly {n} technical/behavioral questions to test these areas.
        Output ONLY a JSON array of strings, e.g., ["Question 1", "Question 2"].
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            content = response['message']['content']
            # Attempt to parse JSON
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != -1:
                return json.loads(content[start:end])
            else:
                # Fallback parsing
                return [line.strip() for line in content.split('\n') if '?' in line][:n]
        except Exception as e:
            print(f"Error generating questions: {e}")
            return ["Tell me about your most challenging project.", "How do you handle deadlines?"]

    def generate_followup_question(self, history: List[Dict[str, str]], last_answer: str) -> str:
        """Generates a follow-up question based on the conversation history."""
        # Construct context from history
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-4:]])
        
        prompt = f"""
        {self.system_prompt}
        
        Recent Conversation:
        {conversation_text}
        
        Candidate's Last Answer: "{last_answer}"
        
        Based on the answer, generate the next relevant follow-up question. If the answer was good, move to a new topic.
        Output ONLY the question text.
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            return response['message']['content'].strip()
        except Exception:
            return "Could you elaborate on that?"

    def analyze_response(self, question: str, answer: str) -> str:
        """Analyzes a single response for quality."""
        prompt = f"""
        Question: {question}
        Answer: {answer}
        
        Rate this answer as 'Strong', 'Average', or 'Weak' and provide a 1-sentence reason.
        Format: "Rating: Reason"
        """
        try:
            response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
            return response['message']['content'].strip()
        except Exception:
            return "Analysis unavailable."

# Singleton
interview_agent = InterviewAgent()
