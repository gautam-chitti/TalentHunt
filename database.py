import sqlite3
import json
from datetime import datetime

DB_FILE = "candidates.db"

def init_db():
    """Initializes the database and creates the candidates table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                years_experience TEXT,
                desired_positions TEXT,
                location TEXT,
                tech_stack TEXT,
                technical_answers TEXT,
                sentiment_analysis TEXT,
                submission_time TEXT
            )
        """)
        conn.commit()

def save_candidate(data: dict) -> int:
    """Saves a candidate's data to the database and returns the new record ID."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO candidates (
                full_name, email, phone, years_experience, desired_positions,
                location, tech_stack, technical_answers, sentiment_analysis, submission_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("full_name"),
            data.get("email"),
            data.get("phone"),
            data.get("years_experience"),
            data.get("desired_positions"),
            data.get("location"),
            data.get("tech_stack"),
            json.dumps(data.get("technical_answers", {})),
            data.get("sentiment_analysis"),
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        return cursor.lastrowid

def view_all_candidates():
    """Retrieves all candidate records from the database."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM candidates ORDER BY submission_time DESC")
        return cursor.fetchall()
