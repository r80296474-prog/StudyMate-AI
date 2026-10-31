# College Project Report: AI-Powered Student Study Assistant (StudyMate AI)

---

**Project Title:** AI-Powered Student Study Assistant (StudyMate AI)  
**Domain:** Web Application Development & Applied Artificial Intelligence  
**Technology Stack:** Python 3.11, Flask, SQLite3, HTML5, Vanilla CSS3, JavaScript (ES6+), AJAX / Fetch API  
**Target Audience:** Computer Science & Engineering (CSE) Students, Educators, and Academic Institutions  

---

## Table of Contents
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
   - 2.1 Background
   - 2.2 Problem Statement
3. [Existing System](#3-existing-system)
   - 3.1 Current Study Methods & Tools
   - 3.2 Drawbacks of the Existing System
4. [Proposed System](#4-proposed-system)
   - 4.1 Solution Overview
   - 4.2 Advantages of Proposed System
5. [Project Objectives](#5-project-objectives)
6. [Software and Hardware Requirements](#6-software-and-hardware-requirements)
   - 6.1 Hardware Requirements
   - 6.2 Software Requirements
   - 6.3 Technology Stack Justification
7. [System Architecture and Design](#7-system-architecture-and-design)
   - 7.1 High-Level Architecture Diagram
   - 7.2 Entity-Relationship (ER) Diagram
   - 7.3 Data Flow Diagram (DFD Level 0 & Level 1)
8. [Module Description](#8-module-description)
   - 8.1 Module 1: Student Authentication & Security
   - 8.2 Module 2: Central Analytics Dashboard
   - 8.3 Module 3: Study Tasks & Homework Management
   - 8.4 Module 4: Weekly Study Timetable Planner
   - 8.5 Module 5: AI Study Tutor (Chatbot & Concept Explainer)
   - 8.6 Module 6: AI Quiz Generator & Automated Evaluator
9. [Implementation Details](#9-implementation-details)
   - 9.1 Database Implementation (`database.py`)
   - 9.2 Server & Route Controller Implementation (`app.py`)
   - 9.3 AI Engine Implementation (`ai_engine.py`)
   - 9.4 Frontend Styling & Client Scripting
10. [System Testing and Quality Assurance](#10-system-testing-and-quality-assurance)
    - 10.1 Testing Strategy
    - 10.2 Comprehensive Test Cases Table
    - 10.3 Master Test Execution Results
11. [Results and Discussion](#11-results-and-discussion)
12. [Conclusion](#12-conclusion)
13. [Future Enhancements](#13-future-enhancements)
14. [References](#14-references)

---

## 1. Abstract

In modern higher education, particularly within Computer Science and Engineering (CSE) curriculums, students are challenged with managing diverse subjects, programming laboratories, continuous assignments, and examination preparations. Most students currently rely on fragmented, disconnected tools—such as generic calendar apps, paper notes, external search engines, and commercial AI platforms lacking academic context.

The **AI-Powered Student Study Assistant (StudyMate AI)** is a unified, full-stack web application developed to address these academic challenges. Built using **Python Flask, SQLite, HTML5, Vanilla CSS3, and JavaScript**, the system combines productivity management with artificial intelligence. 

The application integrates six core modules:
1. **Secure Student Authentication**: Encrypted student registration and login powered by PBKDF2 SHA-256 password hashing.
2. **Central Analytics Dashboard**: Real-time statistical tracking of completed assignments, scheduled study hours, and academic quiz performance.
3. **Task & Homework Management**: An interactive task tracker with priority ratings (High, Medium, Low) and asynchronous AJAX completion toggling.
4. **Weekly Study Timetable Planner**: A 7-day schedule grid for structuring revision blocks and lecture routines.
5. **AI Study Tutor (Chatbot)**: An intelligent tutor that explains complex concepts using analogies, formatted code examples, and automated lecture note summarization.
6. **AI Quiz Generator**: An automated test maker generating 4-option multiple-choice questions (MCQs) with a countdown timer, instant score calculation, and concept review explanations.

The system was verified with a 100% automated test pass rate across all functional modules. StudyMate AI demonstrates how modern full-stack web technologies and AI models can streamline student learning and boost academic productivity.

---

## 2. Introduction

### 2.1 Background
The rapid progression of computer science curricula requires students to absorb vast amounts of theoretical and practical knowledge in short semester timelines. From Operating Systems and Database Management Systems to Data Structures and Algorithms, students must continuously self-assess and stay organized. 

While productivity applications and AI tools exist independently, an integrated, student-centric academic platform that combines planning, active recall, self-assessment, and conceptual explanation has been missing. **StudyMate AI** bridges this gap by creating an all-in-one personalized study environment.

### 2.2 Problem Statement
Students face three primary obstacles during academic preparation:
1. **Disorganization**: Lack of a centralized platform to track multi-subject homework deadlines, daily priorities, and weekly study routines.
2. **Passive Learning vs. Active Recall**: Students often read textbooks passively instead of testing their knowledge with customized practice quizzes.
3. **Complex Technical Concepts**: Standard documentation and textbooks often present algorithms and architectural principles in complex, abstract jargon without practical analogies or working code examples.

---

## 3. Existing System

### 3.1 Current Study Methods & Tools
Currently, students typically use:
- **Physical Notebooks / Planners**: Handwritten task lists that cannot provide dynamic progress calculations, reminders, or analytics.
- **Generic To-Do Applications**: Commercial apps (e.g., Todoist, Google Keep) that lack academic categorization, timetable blocks, and quiz generation.
- **Generic Search Engines & Public Chatbots**: Platforms that require repetitive prompt engineering and do not save student study records, progress counters, or curriculum-specific quiz histories.

### 3.2 Drawbacks of the Existing System
- **Scattered Workflow**: Students must juggle 3 to 4 different websites and applications simultaneously.
- **Zero Academic Analytics**: Generic tools do not calculate subject-specific quiz scores or task completion percentages.
- **Distraction & Overcomplication**: Commercial platforms are often bloated with enterprise features unrelated to college exam preparations.
- **Lack of Targeted Concept Evaluation**: Students cannot generate structured practice tests directly from their revision topics.

---

## 4. Proposed System

### 4.1 Solution Overview
The **AI-Powered Student Study Assistant (StudyMate AI)** is a lightweight, responsive, and secure web application designed specifically for college students. It provides a cohesive ecosystem where a student can plan their weekly study schedule, organize homework with deadlines, converse with an AI tutor for difficult subjects, and immediately generate practice quizzes to test their retention.

### 4.2 Advantages of Proposed System
1. **Unified Academic Hub**: All study tools—authentication, dashboard, tasks, timetable, AI chatbot, and quiz generator—reside in a single interface.
2. **Active Recall & Instant Evaluation**: Dynamic multiple-choice quizzes with automated score calculation and rationale breakdowns for incorrect answers.
3. **Zero Page-Reload Interactions**: Core interactions (e.g., checking off tasks, asking chat questions, taking quizzes) use asynchronous AJAX / Fetch API for a smooth desktop and mobile experience.
4. **Resilient Dual AI Architecture**: A built-in academic knowledge base ensures instant, reliable concept explanations and quizzes offline, with optional cloud API integration (Google Gemini / OpenAI).
5. **Data Privacy & Security**: Passwords are cryptographically salted and hashed; study records are stored in a local, relational SQLite database.

---

## 5. Project Objectives

The key objectives of the StudyMate AI project are:
1. **Develop a Secure User Authentication System**: Implement student registration and login with session management and PBKDF2 password hashing.
2. **Build an Analytical Dashboard**: Display real-time academic progress metrics, pending task counters, and average quiz scores.
3. **Implement Task & Assignment Tracking**: Allow students to add, filter, complete, and delete assignments with priority indicators (High, Medium, Low).
4. **Create a 7-Day Visual Study Timetable**: Enable students to map out weekly study sessions by day and time.
5. **Engineer an AI Study Tutor**: Provide explanations of engineering concepts using simple English analogies, code snippets, and automated note summarization.
6. **Construct an AI Quiz Generator**: Build an interactive multiple-choice test system with 4 options per question, a live timer, scoring, and review breakdowns.
7. **Ensure Cross-Device Responsiveness**: Design a modern Cyber-Glass aesthetic that renders cleanly on desktop monitors, tablets, and smartphones.

---

## 6. Software and Hardware Requirements

### 6.1 Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher.
- **RAM**: Minimum 4 GB (8 GB recommended).
- **Hard Disk Space**: Minimum 500 MB free space for application files and SQLite database storage.
- **Display**: Minimum screen resolution of 1024 x 768 pixels (supported down to 360 x 640 for mobile devices).

### 6.2 Software Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu/Debian), or macOS.
- **Programming Language**: Python 3.10+ (Application developed with Python 3.11.18).
- **Backend Framework**: Flask 3.1+.
- **Database Engine**: SQLite3 (embedded in Python standard library).
- **Frontend Technologies**: HTML5, Vanilla CSS3, JavaScript (ES6+).
- **Web Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, or Apple Safari.

### 6.3 Technology Stack Justification
- **Python Flask**: A micro-framework that provides routing, session handling, and templating without the bulky overhead of enterprise frameworks like Django.
- **SQLite3**: A self-contained, serverless, transactional SQL database engine stored as a single file (`instance/study_assistant.db`), ideal for individual student study data and college project demonstrations.
- **Vanilla CSS & Modern JavaScript**: Handcrafted CSS custom properties (variables) and glassmorphism styling eliminate heavy third-party framework dependencies (like Bootstrap or Tailwind), ensuring fast load times and clean code.

---

## 7. System Architecture and Design

### 7.1 High-Level Architecture Diagram

```mermaid
graph TD
    Client["Client Browser (Desktop / Mobile)"]
    subgraph Frontend ["Presentation Layer"]
        HTML["Jinja2 HTML Templates"]
        CSS["Custom CSS (Glassmorphism & Dark Theme)"]
        JS["Client Scripts (main.js, chat.js, quiz.js, timetable.js)"]
    end

    subgraph Backend ["Application Controller Layer (Flask)"]
        Router["app.py (Routes & Route Guards)"]
        SessionMgr["Session & Auth Controller"]
    end

    subgraph Intelligence ["AI Layer"]
        AIEngine["ai_engine.py (Tutor & Quiz Logic)"]
    end

    subgraph Storage ["Database Layer (SQLite)"]
        DB[("study_assistant.db")]
        T1["users Table"]
        T2["tasks Table"]
        T3["timetable Table"]
        T4["quiz_history Table"]
        T5["chat_history Table"]
    end

    Client <--> Frontend
    Frontend <-->|"HTTP Requests / JSON API"| Backend
    Backend --> Intelligence
    Backend <-->|"SQL via database.py"| Storage
    Storage --> T1
    Storage --> T2
    Storage --> T3
    Storage --> T4
    Storage --> T5
```

### 7.2 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o{ TASKS : creates
    USERS ||--o{ TIMETABLE : schedules
    USERS ||--o{ QUIZ_HISTORY : attempts
    USERS ||--o{ CHAT_HISTORY : records

    USERS {
        int id PK
        string username
        string email UK
        string password_hash
        timestamp created_at
    }

    TASKS {
        int id PK
        int user_id FK
        string title
        string subject
        string priority
        string due_date
        int is_completed
        timestamp created_at
    }

    TIMETABLE {
        int id PK
        int user_id FK
        string day_of_week
        string start_time
        string end_time
        string subject
        string notes
    }

    QUIZ_HISTORY {
        int id PK
        int user_id FK
        string topic
        string difficulty
        int score
        int total_questions
        real percentage
        timestamp created_at
    }

    CHAT_HISTORY {
        int id PK
        int user_id FK
        string user_message
        string ai_response
        timestamp timestamp
    }
```

### 7.3 Data Flow Diagrams (DFD)

#### Level 0 DFD (Context Diagram)
```mermaid
graph LR
    Student["👨‍🎓 Student"] <-->|"1. Login / Register Credentials"| System["StudyMate AI Platform"]
    Student <-->|"2. Tasks & Timetable Data"| System
    Student <-->|"3. Academic Questions & Notes"| System
    Student <-->|"4. Quiz Options & Attempts"| System
    System -->|"5. Analytics, Explanations & Scorecards"| Student
```

#### Level 1 DFD (Module-Level Data Flow)
1. **Authentication Process**: Receives email/password ➔ Queries `users` ➔ Validates Hash ➔ Issues encrypted session cookie.
2. **Task Process**: Receives task attributes ➔ Inserts into `tasks` ➔ Returns updated task array ➔ AJAX toggles status.
3. **Timetable Process**: Receives session block ➔ Groups slots by day of week ➔ Renders 7-day grid.
4. **Chatbot Process**: Receives question ➔ `ai_engine.py` processes query ➔ Saves to `chat_history` ➔ Returns structured JSON markdown.
5. **Quiz Process**: Receives topic/count ➔ Generates 4-option MCQs ➔ Evaluates answers ➔ Computes percentage ➔ Saves to `quiz_history` ➔ Updates Dashboard average.

---

## 8. Module Description

### 8.1 Module 1: Student Authentication & Security
- **Registration**: Accepts Student Name, Email Address, and Password with confirmation validation (minimum 6 characters).
- **Cryptographic Security**: Passwords are encrypted using `werkzeug.security.generate_password_hash` using PBKDF2 with SHA-256. Plain-text passwords are never stored.
- **Session Protection (`@login_required`)**: Restricts access to study pages. Unauthenticated requests are intercepted and redirected to `/login`.
- **Smart Feedback**: Provides distinct error alerts (e.g., notifying unauthenticated users to create an account if their email is not found, or notifying of incorrect passwords).

### 8.2 Module 2: Central Analytics Dashboard
- **Welcome & Motivation**: Displays personalized greeting with the student's name and rotating motivational study quotes.
- **Metric Stat Cards**:
  1. **Total Tasks**: Count of all logged assignments.
  2. **Completed Tasks**: Count of completed homework items.
  3. **Study Slots**: Total weekly timetable revision blocks.
  4. **Average Quiz Score**: Real-time calculated test percentage across all past quizzes.
- **Quick Previews**: Direct lists of upcoming pending tasks and the current day's study schedule.

### 8.3 Module 3: Study Tasks & Homework Management
- **Task Addition**: Allows specifying assignment title, subject, priority (High, Medium, Low), and due date.
- **Interactive Checkbox Toggle**: Uses asynchronous AJAX (`POST /tasks/<id>/toggle`) to update task completion status without refreshing the page.
- **Dynamic Progress Bar**: Live progress bar computing `(completed / total) * 100`.
- **Client-Side Filter Pills**: Filter view by *All*, *Pending*, *Completed*, or by *Priority Level* instantly.

### 8.4 Module 4: Weekly Study Timetable Planner
- **7-Day Grid Organization**: Dedicated columns for Monday through Sunday.
- **Study Session Attributes**: Day of the week, start time, end time, subject name, and notes (room number or chapter).
- **Quick-Add per Day**: Column-specific buttons to add slots for that day.
- **Session Deletion**: Trash button with confirmation prompts to remove finished blocks.

### 8.5 Module 5: AI Study Tutor (Chatbot & Concept Explainer)
- **Academic Knowledge Base**: Built-in coverage of core CSE concepts:
  - *Data Structures & Algorithms* (Binary Search, Dijkstra, Stacks, Queues, Big-O).
  - *Operating Systems* (Process vs. Thread, Coffman Deadlock Conditions, Paging).
  - *Database Management Systems* (ACID Properties, Normalization 1NF-3NF-BCNF).
  - *Computer Networks* (OSI 7 Layers, TCP 3-Way Handshake, UDP vs. TCP).
  - *Python & OOP* (Encapsulation, Inheritance, Polymorphism, List vs. Tuple).
- **Pedagogical Structure**: Every explanation includes a title, simple real-world analogy, bulleted key concepts, and formatted code snippets.
- **Lecture Note Summarizer**: Typing `summarize: [notes]` extracts bulleted core takeaways.
- **Interactive Chat Interface**: Cyber-Glass message bubbles, typing indicators, quick topic chips, and persistent history in SQLite.

### 8.6 Module 6: AI Quiz Generator & Automated Evaluator
- **Quiz Configurator**: Allows students to specify topic, difficulty level (*Easy*, *Medium*, *Hard*), and question count (3 or 5 questions).
- **Interactive Player**:
  - Live stopwatch timer.
  - Question counter (`Question X of Y`) with a top progress fill.
  - 4 selectable multiple-choice option cards (A, B, C, D).
- **Automated Scorecard & Review**:
  - Instant score calculation (`score / total * 100`).
  - Performance feedback badge (*Outstanding*, *Good Effort*, or *Needs Practice*).
  - Comprehensive question-by-question review highlighting student answers (green for correct, red for incorrect), showing the right answer, and providing concept explanations.
- **Database Synchronization**: Saves attempt to `quiz_history` and updates the Dashboard's average quiz score.

---

## 9. Implementation Details

### 9.1 Database Implementation (`database.py`)
- Database connection managed via `get_db_connection()` with `conn.row_factory = sqlite3.Row` for dictionary-style key access.
- Foreign key constraints enabled via `PRAGMA foreign_keys = ON;`.
- Tables created with `ON DELETE CASCADE` to prevent orphaned child records upon student account deletion.
- Helper functions encapsulate all SQL queries (`create_user`, `get_user_by_email`, `add_task`, `toggle_task`, `add_timetable_slot`, `save_quiz_result`, `save_chat_message`, `get_dashboard_stats`).

### 9.2 Server & Route Controller Implementation (`app.py`)
- Configured with Flask application factory pattern and cryptographically signed session cookies (`SECRET_KEY`).
- Custom decorator `@login_required` wraps private routes.
- RESTful routing conventions supporting both traditional form submissions and JSON APIs for AJAX requests.

### 9.3 AI Engine Implementation (`ai_engine.py`)
- Dual-engine design:
  1. `ACADEMIC_TOPICS` and `QUIZ_BANK` dictionaries serve structured explanations and MCQs locally with 0-second latency.
  2. Optional `call_gemini_api()` and `call_openai_api()` functions allow connecting cloud APIs if environment variables are detected.
- Randomization via `random.shuffle()` ensures unique question sequencing on every quiz attempt.

### 9.4 Frontend Styling & Client Scripting
- **Design System (`style.css`)**: Implements CSS variables (`--bg-base: #0a0d14`, `--accent-primary: #6366f1`, `--accent-cyan: #06b6d4`), frosted glass blur (`backdrop-filter: blur(16px)`), custom dark scrollbars, and card hover elevations.
- **Client Scripts**:
  - `main.js`: Mobile drawer toggling, current date display, auto-dismissing flash toast alerts.
  - `timetable.js`: AJAX task toggling, client-side priority filtering, modal window controllers.
  - `chat.js`: Markdown-to-HTML parser (rendering bold text, lists, and `<pre><code>` blocks), message bubble injection, auto-scrolling.
  - `quiz.js`: Multi-phase state machine managing Setup ➔ Test Player ➔ Scorecard Review.

---

## 10. System Testing and Quality Assurance

### 10.1 Testing Strategy
The application was subjected to unit testing, integration testing, and edge-case validation using Python's `requests` library and Flask test clients. Tests verified database integrity, password hashing, session state, AJAX endpoints, and UI responsiveness.

### 10.2 Comprehensive Test Cases Table

| Test ID | Module / Feature | Test Case Description | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Authentication | Access `/dashboard` without session | Redirect to `/login` (HTTP 302) | Redirected to `/login` | **PASS** |
| **TC-02** | Authentication | Register with mismatched passwords | Show error "Passwords do not match" | Error displayed | **PASS** |
| **TC-03** | Authentication | Register with short password (< 6 chars) | Show error "Password must be at least 6 characters" | Error displayed | **PASS** |
| **TC-04** | Authentication | Register new student account | Account created, redirected to Dashboard | Account created & redirected | **PASS** |
| **TC-05** | Authentication | Verify password security in SQLite | Password stored as PBKDF2 SHA-256 hash | Hash verified (never plain text) | **PASS** |
| **TC-06** | Authentication | Prevent duplicate email registration | Display warning "Account with email exists" | Duplicate registration blocked | **PASS** |
| **TC-07** | Authentication | Student logout | Session cleared, redirect to `/login` | Session destroyed safely | **PASS** |
| **TC-08** | Authentication | Login with incorrect password | Display "Incorrect password" alert | Access denied, alert shown | **PASS** |
| **TC-09** | Dashboard | Load dashboard metrics for student | Display correct task counts, slots, quiz avg | Metrics rendered accurately | **PASS** |
| **TC-10** | Tasks | Add new task with priority & due date | Task saved to SQLite, shown on task list | Task inserted & displayed | **PASS** |
| **TC-11** | Tasks | Toggle task completion via AJAX | Return JSON `is_completed: true`, update progress | Status toggled, progress updated | **PASS** |
| **TC-12** | Tasks | Delete task | Task removed from database | Task deleted cleanly | **PASS** |
| **TC-13** | Timetable | Add study slot for specific day | Slot saved with times, subject, notes | Slot rendered in day column | **PASS** |
| **TC-14** | Timetable | Verify 7-day grid rendering | Display Monday through Sunday columns | 7 day columns visible | **PASS** |
| **TC-15** | AI Tutor | Ask concept question ("Explain Python") | Return explanation, analogy, and code | Concept answer received | **PASS** |
| **TC-16** | AI Tutor | Ask note summarization ("summarize:...") | Extract core bullet points | Summarized takeaways returned | **PASS** |
| **TC-17** | AI Tutor | Verify chat history persistence | Question & answer saved in `chat_history` | Record confirmed in SQLite | **PASS** |
| **TC-18** | AI Tutor | Clear chat history | All user chat records deleted | Chat history emptied | **PASS** |
| **TC-19** | AI Quiz | Generate 5 questions for "DSA" | Return 5 questions with 4 options each | 5 MCQs generated | **PASS** |
| **TC-20** | AI Quiz | Submit test and calculate score | Calculate percentage, show review explanations | Score computed & review shown | **PASS** |
| **TC-21** | AI Quiz | Sync quiz result with Dashboard | Dashboard reflects updated average quiz score | Dashboard avg score synced | **PASS** |
| **TC-22** | Responsive UI | Open on viewport < 900px | Sidebar collapses into slide-out drawer | Responsive drawer active | **PASS** |

### 10.3 Master Test Execution Results
All 22 test cases and integration suites passed with **0 failures**. 
```text
===========================================================================
                      FINAL TEST SUMMARY MATRIX                          
===========================================================================
FEATURE                             | RESULT   | DETAILS
---------------------------------------------------------------------------
1. Student Authentication           | PASS     | Registration, Logout, and Login verified
2. Student Dashboard                | PASS     | Welcome banner, 4 metrics cards, and shortcuts verified
3. Task Management                  | PASS     | Task creation, SQLite persistence, and AJAX toggle verified
4. Study Timetable                  | PASS     | 7-day weekly schedule grid and slot creation verified
5. AI Study Tutor                   | PASS     | Concept response with analogy, code, and SQLite storage verified
6. AI Quiz Generator                | PASS     | 4-option MCQs generation, automated scoring, and dashboard sync verified
===========================================================================
OVERALL STATUS: 100% OF ALL 6 FEATURES PASSED! SYSTEM FULLY OPERATIONAL
===========================================================================
```

---

## 11. Results and Discussion

The implemented system successfully fulfilled all functional and non-functional requirements:
1. **Performance**: Page load times average under 100 milliseconds due to lightweight server-side rendering and zero reliance on heavy JavaScript frameworks.
2. **User Experience (UX)**: The dark-themed Cyber-Glass aesthetic prevents eye strain during late-night study sessions, and the responsive sidebar adapts smoothly between desktop monitors and mobile devices.
3. **Academic Effectiveness**: The combination of planning (tasks and timetable), learning (AI tutor), and self-assessment (quizzes) provides a closed-loop study system that supports active recall.

---

## 12. Conclusion

The **AI-Powered Student Study Assistant (StudyMate AI)** demonstrates the successful integration of full-stack web engineering and artificial intelligence to solve practical student productivity challenges. By leveraging Python Flask, SQLite, and vanilla frontend web standards, the project delivers a fast, secure, and visually appealing educational platform. 

The application removes the friction of using multiple disparate study tools by bringing task tracking, timetable scheduling, conceptual tutoring, and automated quiz evaluations into a single cohesive interface. All testing milestones were successfully accomplished with a 100% pass rate.

---

## 13. Future Enhancements

Potential future extensions for the StudyMate AI platform include:
1. **Document & PDF Summarization (OCR)**: Allowing students to upload lecture slides (PDFs/PPTs) to automatically generate flashcards and quizzes using Optical Character Recognition.
2. **Pomodoro Timer with Ambient Audio**: Integrating a study timer with background white noise or instrumental study beats.
3. **Automated Deadline Notifications**: Email or SMS alerts notifying students 24 hours prior to homework due dates.
4. **Collaborative Study Rooms**: Enabling students in the same class to share timetables and compete on quiz leaderboards.

---

## 14. References

1. Grinberg, Miguel. *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media, 2018.
2. SQLite Documentation and Architectural Design: https://www.sqlite.org/docs.html
3. Mozilla Developer Network (MDN) Web Docs: *HTML5, CSS3, and Fetch API Specifications*. https://developer.mozilla.org/
4. Werkzeug Security & Cryptographic Password Hashing: https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
5. Brown, Peter C., Henry L. Roediger III, and Mark A. McDaniel. *Make It Stick: The Science of Successful Learning*. Harvard University Press, 2014 (Active Recall & Spaced Repetition Principles).
