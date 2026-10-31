"""
app.py - Main Flask Application for AI-Powered Student Study Assistant
Handles Routing, Student Authentication, and Session Management.
"""

import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import database
import ai_engine

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'studymate_secure_development_key_2026')


def login_required(f):
    """
    Decorator to protect routes that require a logged-in student.
    Redirects to the login page if session['user_id'] is not found.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in first to access your study tools.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def index():
    """Root URL: Redirects to dashboard if logged in, else to login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles student sign-in with email and password."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        # Validation
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('login.html', active_tab='login')

        user = database.get_user_by_email(email)

        # Check credentials with helpful, specific feedback
        if not user:
            flash("No account found with this email. Click 'Create Account' below to sign up!", "warning")
            return render_template('login.html', active_tab='register')

        if check_password_hash(user['password_hash'], password):
            # Store student info in session cookie
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            flash(f"Welcome back, {user['username']}! Let's get to studying.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect password. Please double-check your password.", "danger")
            return render_template('login.html', active_tab='login')

    return render_template('login.html', active_tab='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles new student account registration."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    # If student visits /register directly via URL
    if request.method == 'GET':
        return render_template('login.html', active_tab='register')

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    # Form Validations
    if not username or not email or not password or not confirm_password:
        flash("All fields are required to create an account.", "danger")
        return render_template('login.html', active_tab='register')

    if len(password) < 6:
        flash("Password must be at least 6 characters long.", "danger")
        return render_template('login.html', active_tab='register')

    if password != confirm_password:
        flash("Passwords do not match. Please re-enter carefully.", "danger")
        return render_template('login.html', active_tab='register')

    # Check if student email is already registered
    existing_user = database.get_user_by_email(email)
    if existing_user:
        flash("An account with this email already exists. Please sign in.", "warning")
        return render_template('login.html', active_tab='login')

    # Hash the password securely using PBKDF2 with SHA-256
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Save to SQLite database
    user_id = database.create_user(username, email, password_hash)
    if user_id:
        # Automatically log the student in
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
        flash(f"Welcome to StudyMate AI, {username}! Your account is ready.", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("This username or email is already taken. Please try another.", "danger")
        return render_template('login.html', active_tab='register')


@app.route('/logout')
def logout():
    """Logs the student out and clears their session."""
    username = session.get('username', 'Student')
    session.clear()
    flash(f"Goodbye {username}! You have been logged out safely.", "info")
    return redirect(url_for('login'))


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main student dashboard displaying stats, recent tasks, and timetable."""
    user_id = session['user_id']
    user = database.get_user_by_id(user_id)
    stats = database.get_dashboard_stats(user_id)
    recent_tasks = database.get_user_tasks(user_id)[:5]
    timetable_slots = database.get_user_timetable(user_id)

    return render_template(
        'dashboard.html',
        user=user,
        stats=stats,
        recent_tasks=recent_tasks,
        timetable_slots=timetable_slots
    )


# ==========================================
# FEATURE ROUTE STUBS (Implemented in Steps 6, 7, 8)
# ==========================================

# ==========================================
# AI STUDY CHATBOT ROUTES (Step 7)
# ==========================================

@app.route('/chatbot')
@login_required
def chatbot():
    """AI Study Chatbot Page: renders recent conversation history."""
    user_id = session['user_id']
    chat_history = database.get_user_chats(user_id)
    return render_template('chatbot.html', chat_history=chat_history)


@app.route('/chatbot/ask', methods=['POST'])
@login_required
def chatbot_ask():
    """Processes student question and returns AI response."""
    user_id = session['user_id']
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Generate answer via AI Engine
    reply = ai_engine.get_study_response(user_id, message)

    # Save to SQLite database
    database.save_chat_message(user_id, message, reply)
    timestamp = datetime.now().strftime('%I:%M %p')

    return jsonify({
        'reply': reply,
        'timestamp': timestamp
    })


@app.route('/chatbot/clear', methods=['POST'])
@login_required
def chatbot_clear():
    """Clears conversation history for the student."""
    user_id = session['user_id']
    database.clear_user_chats(user_id)
    return jsonify({'success': True})


# ==========================================
# AI QUIZ GENERATOR ROUTES (Step 8)
# ==========================================

@app.route('/quiz')
@login_required
def quiz():
    """AI Quiz Generator Page: displays quiz configurator and past quiz attempts."""
    user_id = session['user_id']
    past_quizzes = database.get_user_quizzes(user_id, limit=10)
    return render_template('quiz.html', past_quizzes=past_quizzes)


@app.route('/quiz/generate', methods=['POST'])
@login_required
def quiz_generate():
    """Generates multiple-choice quiz questions based on topic and difficulty."""
    data = request.get_json() or {}
    topic = data.get('topic', 'Data Structures').strip()
    difficulty = data.get('difficulty', 'Medium').strip()
    count = int(data.get('count', 5))

    questions = ai_engine.generate_quiz(topic, difficulty, count)
    return jsonify({'questions': questions})


@app.route('/quiz/save', methods=['POST'])
@login_required
def quiz_save():
    """Saves completed quiz results and updates student test record."""
    user_id = session['user_id']
    data = request.get_json() or {}

    topic = data.get('topic', 'General').strip()
    difficulty = data.get('difficulty', 'Medium').strip()
    score = int(data.get('score', 0))
    total_questions = int(data.get('total_questions', 5))

    quiz_id = database.save_quiz_result(user_id, topic, difficulty, score, total_questions)
    return jsonify({
        'success': True,
        'quiz_id': quiz_id
    })


# ==========================================
# STUDY TIMETABLE ROUTES (Step 6)
# ==========================================

@app.route('/timetable')
@login_required
def timetable():
    """Study Timetable Planner Page: displays schedule grouped by day."""
    user_id = session['user_id']
    all_slots = database.get_user_timetable(user_id)
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    slots_by_day = {day: [] for day in days}
    for slot in all_slots:
        day = slot['day_of_week']
        if day in slots_by_day:
            slots_by_day[day].append(slot)

    return render_template('timetable.html', slots_by_day=slots_by_day)


@app.route('/timetable/add', methods=['POST'])
@login_required
def add_timetable_slot_route():
    """Adds a new study block to the weekly schedule."""
    user_id = session['user_id']
    day_of_week = request.form.get('day_of_week', '').strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    subject = request.form.get('subject', '').strip()
    notes = request.form.get('notes', '').strip()

    if not day_of_week or not start_time or not end_time or not subject:
        flash("Please provide day, time range, and subject name.", "danger")
        return redirect(url_for('timetable'))

    database.add_timetable_slot(user_id, day_of_week, start_time, end_time, subject, notes)
    flash(f"Added {subject} study session for {day_of_week} ({start_time} - {end_time})!", "success")
    return redirect(url_for('timetable'))


@app.route('/timetable/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_timetable_slot_route(slot_id):
    """Deletes a study session from the timetable."""
    user_id = session['user_id']
    database.delete_timetable_slot(slot_id, user_id)
    flash("Study session removed from your schedule.", "info")
    return redirect(url_for('timetable'))


# ==========================================
# TASK MANAGEMENT ROUTES (Step 6)
# ==========================================

@app.route('/tasks')
@login_required
def tasks():
    """Tasks & Homework Checklist Page."""
    user_id = session['user_id']
    user_tasks = database.get_user_tasks(user_id)
    
    total_count = len(user_tasks)
    completed_count = sum(1 for t in user_tasks if t['is_completed'])
    pending_count = total_count - completed_count
    progress_percent = round((completed_count / total_count) * 100) if total_count > 0 else 0

    return render_template(
        'tasks.html',
        tasks=user_tasks,
        total_count=total_count,
        completed_count=completed_count,
        pending_count=pending_count,
        progress_percent=progress_percent
    )


@app.route('/tasks/add', methods=['POST'])
@login_required
def add_task_route():
    """Adds a new study task or homework assignment."""
    user_id = session['user_id']
    title = request.form.get('title', '').strip()
    subject = request.form.get('subject', 'General').strip()
    priority = request.form.get('priority', 'Medium').strip()
    due_date = request.form.get('due_date', '').strip() or None

    if not title:
        flash("Task title cannot be empty.", "danger")
        return redirect(url_for('tasks'))

    database.add_task(user_id, title, subject, priority, due_date)
    flash(f"Task '{title}' added successfully! 🚀", "success")
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task_route(task_id):
    """Toggles task status between pending and completed (supports both AJAX and Form)."""
    user_id = session['user_id']
    is_completed = database.toggle_task(task_id, user_id)

    # Recalculate stats for live UI updates
    user_tasks = database.get_user_tasks(user_id)
    total_count = len(user_tasks)
    completed_count = sum(1 for t in user_tasks if t['is_completed'])
    progress_percent = round((completed_count / total_count) * 100) if total_count > 0 else 0

    # If AJAX request from JavaScript
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({
            "success": True,
            "task_id": task_id,
            "is_completed": is_completed,
            "total_tasks": total_count,
            "completed_tasks": completed_count,
            "progress_percent": progress_percent
        })

    # Fallback standard form submission
    return redirect(url_for('tasks'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task_route(task_id):
    """Deletes a study task."""
    user_id = session['user_id']
    database.delete_task(task_id, user_id)
    flash("Task deleted successfully.", "info")
    return redirect(url_for('tasks'))


# ==========================================
# APPLICATION ENTRYPOINT
# ==========================================

if __name__ == '__main__':
    # Ensure database tables exist before serving traffic
    database.init_db()
    print("StudyMate AI Server starting on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
