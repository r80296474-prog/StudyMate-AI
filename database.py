"""
database.py - Database Layer for AI-Powered Student Study Assistant
Handles SQLite database connection, table initialization, and helper queries.
"""

import os
import sqlite3
from datetime import datetime

# Determine the database file path inside the 'instance' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'study_assistant.db')


def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    row_factory = sqlite3.Row allows column access like dictionaries (row['title']).
    """
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign key constraint support in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """
    Initializes all required database tables if they do not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table (Authentication)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Tasks Table (Study To-Do & Assignments)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            subject TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium', -- 'High', 'Medium', 'Low'
            due_date TEXT,
            is_completed INTEGER DEFAULT 0,  -- 0 = pending, 1 = completed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # 3. Timetable Table (Weekly Schedule Planner)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL,       -- 'Monday', 'Tuesday', etc.
            start_time TEXT NOT NULL,        -- e.g. '09:00'
            end_time TEXT NOT NULL,          -- e.g. '10:30'
            subject TEXT NOT NULL,           -- e.g. 'Data Structures'
            notes TEXT DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # 4. Quiz History Table (AI Quiz Results)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Medium',
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    # 5. Chat History Table (AI Study Bot Conversations)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
    print("[SUCCESS] Database tables initialized successfully at:", DB_PATH)


# ==========================================
# USER FUNCTIONS
# ==========================================

def create_user(username, email, password_hash):
    """Inserts a new student account into the users table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None  # Username or email already exists
    finally:
        conn.close()


def get_user_by_email(email):
    """Fetches user details by email (case-insensitive and trimmed)."""
    if not email:
        return None
    conn = get_db_connection()
    email_clean = email.strip().lower()
    user = conn.execute("SELECT * FROM users WHERE LOWER(TRIM(email)) = LOWER(?)", (email_clean,)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Fetches user details by ID."""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


# ==========================================
# TASK FUNCTIONS
# ==========================================

def get_user_tasks(user_id, completed=None):
    """Returns tasks for a given user. Can filter by completed status (0 or 1)."""
    conn = get_db_connection()
    if completed is None:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? ORDER BY is_completed ASC, due_date ASC",
            (user_id,)
        ).fetchall()
    else:
        tasks = conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND is_completed = ? ORDER BY due_date ASC",
            (user_id, completed)
        ).fetchall()
    conn.close()
    return tasks


def add_task(user_id, title, subject="General", priority="Medium", due_date=None):
    """Adds a new study task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, title, subject, priority, due_date) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, subject, priority, due_date)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def toggle_task(task_id, user_id):
    """Toggles task status between 0 (pending) and 1 (completed) and returns new state."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    )
    conn.commit()
    cursor.execute("SELECT is_completed FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    row = cursor.fetchone()
    conn.close()
    return bool(row[0]) if row else False


def delete_task(task_id, user_id):
    """Deletes a task by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()


# ==========================================
# TIMETABLE FUNCTIONS
# ==========================================

def get_user_timetable(user_id):
    """Returns all timetable slots for a user ordered by day and start time."""
    conn = get_db_connection()
    slots = conn.execute(
        """
        SELECT * FROM timetable 
        WHERE user_id = ? 
        ORDER BY 
            CASE day_of_week
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
                ELSE 8
            END,
            start_time ASC
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return slots


def add_timetable_slot(user_id, day_of_week, start_time, end_time, subject, notes=""):
    """Adds a new weekly study schedule slot."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timetable (user_id, day_of_week, start_time, end_time, subject, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, day_of_week, start_time, end_time, subject, notes)
    )
    conn.commit()
    slot_id = cursor.lastrowid
    conn.close()
    return slot_id


def delete_timetable_slot(slot_id, user_id):
    """Deletes a timetable slot."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM timetable WHERE id = ? AND user_id = ?", (slot_id, user_id))
    conn.commit()
    conn.close()


# ==========================================
# QUIZ & CHAT FUNCTIONS
# ==========================================

def save_quiz_result(user_id, topic, difficulty, score, total_questions):
    """Saves a student's quiz attempt and percentage."""
    percentage = round((score / total_questions) * 100, 1) if total_questions > 0 else 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_history (user_id, topic, difficulty, score, total_questions, percentage) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, topic, difficulty, score, total_questions, percentage)
    )
    conn.commit()
    quiz_id = cursor.lastrowid
    conn.close()
    return quiz_id


def get_user_quizzes(user_id, limit=5):
    """Returns recent quiz attempts for the student."""
    conn = get_db_connection()
    quizzes = conn.execute(
        "SELECT * FROM quiz_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return quizzes


def save_chat_message(user_id, user_message, ai_response):
    """Saves conversation history between student and AI bot."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, user_message, ai_response) VALUES (?, ?, ?)",
        (user_id, user_message, ai_response)
    )
    conn.commit()
    chat_id = cursor.lastrowid
    conn.close()
    return chat_id


def get_user_chats(user_id, limit=30):
    """Retrieves recent conversation history."""
    conn = get_db_connection()
    chats = conn.execute(
        "SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return chats


def clear_user_chats(user_id):
    """Clears all conversation history for the student."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ==========================================
# DASHBOARD ANALYTICS FUNCTION
# ==========================================

def get_dashboard_stats(user_id):
    """Calculates overall statistics for the student dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total and completed tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,))
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ? AND is_completed = 1", (user_id,))
    completed_tasks = cursor.fetchone()[0]

    pending_tasks = total_tasks - completed_tasks

    # Timetable slots count
    cursor.execute("SELECT COUNT(*) FROM timetable WHERE user_id = ?", (user_id,))
    total_slots = cursor.fetchone()[0]

    # Quiz statistics
    cursor.execute("SELECT COUNT(*), AVG(percentage) FROM quiz_history WHERE user_id = ?", (user_id,))
    quiz_row = cursor.fetchone()
    total_quizzes = quiz_row[0] or 0
    avg_score = round(quiz_row[1], 1) if quiz_row[1] is not None else 0.0

    conn.close()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_slots": total_slots,
        "total_quizzes": total_quizzes,
        "avg_score": avg_score
    }


if __name__ == "__main__":
    # Test script execution: Initialize tables when executed directly
    init_db()
