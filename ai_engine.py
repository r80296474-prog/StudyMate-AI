"""
ai_engine.py - AI Study Engine for Student Study Assistant
Powers the AI Study Tutor (Chatbot) and AI Quiz Generator.
Supports offline heuristic academic engine with optional Gemini / OpenAI API integration.
"""

import os
import re
import json
import random
import requests

# Load optional API keys from environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ===================================================================
# BUILT-IN ACADEMIC KNOWLEDGE BASE (CSE & GENERAL STUDY TOPICS)
# Provides detailed, structured explanations with real-world analogies
# ===================================================================

ACADEMIC_TOPICS = {
    "binary search": {
        "title": "Binary Search Algorithm",
        "analogy": "Imagine searching for a word in a 1,000-page dictionary. You don't read from page 1 to 1000. You open the middle (page 500). If your word comes earlier alphabetically, you ignore the second half and check page 250. You cut the search space in half at every step!",
        "points": [
            "**Prerequisite**: The list or array **MUST be sorted** in ascending or descending order.",
            "**Time Complexity**: Best Case: O(1), Average/Worst Case: **O(log n)**.",
            "**Space Complexity**: O(1) for iterative, O(log n) for recursive call stack."
        ],
        "code": "def binary_search(arr, target):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1"
    },
    "process vs thread": {
        "title": "Process vs. Thread (Operating Systems)",
        "analogy": "Think of a **Process** like a whole house with its own kitchen, bathroom, and electricity. A **Thread** is like an individual person living inside that house—family members share the kitchen and rooms (memory), but each person has their own tasks.",
        "points": [
            "**Process**: An independent executing program with its own dedicated memory space (code, data, heap, stack). Creating and switching processes is heavyweight.",
            "**Thread**: The smallest unit of CPU execution inside a process. Threads within the same process share the same memory and file descriptors, making context switching very lightweight.",
            "**Crash Impact**: If one process crashes, other processes are unaffected. If a thread crashes unexpectedly with a segmentation fault, it can crash the entire parent process."
        ],
        "code": None
    },
    "acid": {
        "title": "ACID Properties in Databases (DBMS)",
        "analogy": "Think of transferring $100 from Account A to Account B via ATM. You need Account A to decrease by $100 and Account B to increase by $100. If the power cuts mid-way, either the whole transfer completes, or no money leaves Account A. That is ACID!",
        "points": [
            "**A - Atomicity**: 'All or nothing.' Every statement in a transaction must succeed; otherwise, the entire transaction rolls back.",
            "**C - Consistency**: The database moves from one valid state to another valid state, maintaining all constraints (foreign keys, balances >= 0).",
            "**I - Isolation**: Concurrent transactions execute as if they are running sequentially without interfering with each other.",
            "**D - Durability**: Once a transaction is committed, its changes are permanently written to non-volatile storage, surviving system crashes."
        ],
        "code": None
    },
    "normalization": {
        "title": "Database Normalization (1NF, 2NF, 3NF, BCNF)",
        "analogy": "Imagine organizing a messy closet where shirts, socks, and books are tossed together in one drawer (data redundancy & anomalies). Normalization is separating them into dedicated, labeled drawers connected by pointers.",
        "points": [
            "**1NF (First Normal Form)**: Eliminate duplicate columns and ensure all attributes contain **atomic (indivisible) values**.",
            "**2NF (Second Normal Form)**: Must be in 1NF, and eliminate **partial dependency** (every non-key attribute must depend on the whole primary key, not part of a composite key).",
            "**3NF (Third Normal Form)**: Must be in 2NF, and eliminate **transitive dependency** (non-key attributes should not depend on other non-key attributes: X → Y → Z).",
            "**BCNF (Boyce-Codd Normal Form)**: A stricter 3NF where for every functional dependency X → Y, **X must be a super key**."
        ],
        "code": None
    },
    "dijkstra": {
        "title": "Dijkstra's Shortest Path Algorithm",
        "analogy": "Think of Google Maps finding the shortest route from your college campus to the airport. Dijkstra visits the nearest unexplored intersection first, updates travel distances to neighbors, and never re-checks an already settled route.",
        "points": [
            "**Purpose**: Finds the shortest path from a single source node to all other vertices in a weighted graph.",
            "**Constraint**: Edge weights **MUST be non-negative** (use Bellman-Ford if negative edges exist).",
            "**Data Structure**: Implemented efficiently using a **Min-Priority Queue (Binary Heap)**.",
            "**Time Complexity**: O((V + E) log V) with a Min-Heap, where V is vertices and E is edges."
        ],
        "code": "import heapq\n\ndef dijkstra(graph, start):\n    distances = {node: float('inf') for node in graph}\n    distances[start] = 0\n    pq = [(0, start)]\n    \n    while pq:\n        cur_dist, u = heapq.heappop(pq)\n        if cur_dist > distances[u]:\n            continue\n        for neighbor, weight in graph[u].items():\n            distance = cur_dist + weight\n            if distance < distances[neighbor]:\n                distances[neighbor] = distance\n                heapq.heappush(pq, (distance, neighbor))\n    return distances"
    },
    "tcp vs udp": {
        "title": "TCP vs. UDP Protocol Comparison (Computer Networks)",
        "analogy": "TCP is like a **Registered Post Package** with signature confirmation: every box is tracked, guaranteed delivered in order, and resent if lost. UDP is like a **Live Television Broadcast**: fast and continuous, but if a frame glitches, the stream keeps going without resending.",
        "points": [
            "**TCP (Transmission Control Protocol)**: Connection-oriented (3-Way Handshake: SYN, SYN-ACK, ACK), reliable delivery, ordered packets, flow control, and error recovery. Used in HTTP/HTTPS, SSH, FTP, Email.",
            "**UDP (User Datagram Protocol)**: Connectionless, unreliable (best-effort), no packet ordering, minimal header overhead (8 bytes vs 20 bytes). Used in Live Video Streaming, Online Gaming (FPS), DNS, VoIP."
        ],
        "code": None
    },
    "oop": {
        "title": "4 Pillars of Object-Oriented Programming (OOP)",
        "analogy": "Think of a Smartphone: You press the volume button without knowing the internal micro-circuits (Abstraction). All components are sealed inside a casing (Encapsulation). An iPhone and Android are both types of Smartphones (Inheritance). The power button does different things depending on how long you hold it (Polymorphism).",
        "points": [
            "**1. Encapsulation**: Bundling data (variables) and methods that manipulate them into a single unit (class), hiding internal details using access modifiers (private, protected).",
            "**2. Abstraction**: Hiding internal complexity and showing only essential features to the user (e.g. abstract classes and interfaces).",
            "**3. Inheritance**: Mechanism where a child/derived class acquires properties and behavior of a parent/base class, promoting code reusability.",
            "**4. Polymorphism**: 'Many forms.' The ability of a message or function to be processed in more than one way (Method Overloading & Method Overriding)."
        ],
        "code": None
    },
    "study tip": {
        "title": "Scientifically Proven Study Techniques for Engineers",
        "analogy": "Studying for 10 hours straight before an exam is like cramming a week's worth of food into one sitting—your brain simply cannot digest it. Effective learning requires active digestion and retrieval intervals.",
        "points": [
            "**1. The Feynman Technique**: Try explaining the topic in simple terms to a non-technical friend. Whenever you get stuck, re-read that specific section.",
            "**2. Active Recall**: Instead of passively re-reading notes or highlighting text, close the book and quiz yourself or write down everything you remember on a blank paper.",
            "**3. Spaced Repetition**: Review key concepts on Day 1, Day 3, Day 7, and Day 14 to convert short-term memory into permanent long-term memory.",
            "**4. Pomodoro Method**: Study with intense focus for 25 minutes, then take an intentional 5-minute break. Repeat 4 cycles, then take a longer 20-minute rest."
        ],
        "code": None
    },
    "python": {
        "title": "Python Programming in Simple English",
        "analogy": "Imagine giving instructions to a friend in plain English instead of writing complicated legal contracts. In languages like C++ or Java, printing 'Hello World' takes 5-7 lines of boilerplate classes and syntax. In Python, you simply write: print('Hello, World!').",
        "points": [
            "**What is Python?**: A high-level, general-purpose programming language created by Guido van Rossum in 1991. Its core philosophy is that 'Readability Counts'.",
            "**Interpreted & Dynamically Typed**: Code executes line-by-line without manual compilation. You don't have to declare types like `int` or `String`—Python automatically determines the type (e.g., `x = 25`).",
            "**Where is it used?**: Web Development (Flask, Django), Artificial Intelligence & Machine Learning (TensorFlow, PyTorch), Data Science (Pandas, NumPy), Cybersecurity, and Automation Scripting.",
            "**Batteries Included**: Comes with rich built-in libraries for SQLite databases (`sqlite3`), web networking (`urllib`, `requests`), math, and JSON processing."
        ],
        "code": "# Python reads like plain English!\nstudent_name = 'Alex'\nscores = [88, 92, 79, 95]\naverage_score = sum(scores) / len(scores)\n\nprint(f'Hello {student_name}! Your average score is {average_score:.1f}')"
    }
}


def call_gemini_api(prompt):
    """Calls Google Gemini API if GEMINI_API_KEY is configured."""
    if not GEMINI_API_KEY:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"You are StudyMate AI, an encouraging and highly knowledgeable academic tutor for computer science and engineering students. Provide clear, well-structured, easy-to-understand explanations with bullet points and code examples where helpful.\n\nStudent Question: {prompt}"
                }]
            }]
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print("[AI API Warning] Gemini call failed, falling back to local engine:", e)
    return None


def call_openai_api(prompt):
    """Calls OpenAI API if OPENAI_API_KEY is configured."""
    if not OPENAI_API_KEY:
        return None
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are StudyMate AI, an encouraging and expert college study tutor for CSE students. Explain concepts with clarity, analogies, and practical examples."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data['choices'][0]['message']['content']
    except Exception as e:
        print("[AI API Warning] OpenAI call failed, falling back to local engine:", e)
    return None


def generate_local_response(query):
    """
    Intelligent local heuristic academic engine for computer science & study planning.
    Ensures 100% offline uptime and instant answers during college project demonstrations.
    """
    q = query.lower().strip()

    # 1. Check for Note Summarization request
    if q.startswith("summarize:") or q.startswith("notes:") or "summarize" in q or "summary" in q:
        cleaned_text = re.sub(r'^(summarize:?|notes:?)\s*', '', query, flags=re.IGNORECASE).strip()
        sentences = [s.strip() for s in cleaned_text.replace('\n', '. ').split('.') if len(s.strip()) > 15]
        
        if len(sentences) >= 2:
            summary_bullets = "\n".join([f"• **Key Concept {i+1}**: {s}" for i, s in enumerate(sentences[:4])])
            return f"### 📝 Study Summary & Key Takeaways\n\nHere are the most critical points extracted from your notes:\n\n{summary_bullets}\n\n**💡 Exam Tip**: Review these {len(sentences[:4])} core concepts and test yourself using active recall!"
        else:
            return f"### 📝 Notes Summary\n\n**Main Idea**: {cleaned_text}\n\n• **Core Principle**: Focus on understanding the definitions, formulas, and edge cases.\n• **Action Step**: Try explaining this in your own words or generating a quiz on this topic in the Quiz tab!"

    # 2. Check for matching Academic Knowledge Base topics
    for key, data in ACADEMIC_TOPICS.items():
        if key in q:
            response = f"### 🎓 {data['title']}\n\n"
            if data['analogy']:
                response += f"**💡 Simple Analogy**: {data['analogy']}\n\n"
            response += "**📌 Core Concepts to Remember**:\n"
            for pt in data['points']:
                response += f"- {pt}\n"
            if data['code']:
                response += f"\n**💻 Code Implementation**:\n```python\n{data['code']}\n```\n"
            response += "\n*Ask me if you'd like a practice question or deeper dive on this topic!*"
            return response

    # 3. Dynamic Keyword-Based Answers
    if "python" in q and ("difference" in q or "vs" in q or "list" in q):
        return (
            "### 🐍 Python Data Structures: List vs. Tuple\n\n"
            "• **List `[1, 2, 3]`**: **Mutable** (can add, change, or remove elements). Slower iteration, uses more memory.\n"
            "• **Tuple `(1, 2, 3)`**: **Immutable** (cannot be altered once created). Faster iteration, hashable (can be used as dictionary keys).\n\n"
            "```python\nmy_list = [1, 2]\nmy_list.append(3) # Allowed\n\nmy_tuple = (1, 2)\n# my_tuple.append(3) # Raises AttributeError!\n```"
        )

    if "big o" in q or "time complexity" in q:
        return (
            "### ⏱️ Big-O Notation Cheat Sheet\n\n"
            "Big-O measures how runtime or space requirements scale as input size `n` grows:\n\n"
            "1. **O(1) - Constant**: Array index access, Hash map lookup.\n"
            "2. **O(log n) - Logarithmic**: Binary Search on a sorted array.\n"
            "3. **O(n) - Linear**: Iterating through an unsorted array.\n"
            "4. **O(n log n) - Linearithmic**: Merge Sort, Heap Sort, average Quick Sort.\n"
            "5. **O(n²) - Quadratic**: Nested loops (Bubble Sort, Selection Sort).\n"
            "6. **O(2ⁿ) - Exponential**: Recursive Fibonacci without memoization."
        )

    if "stack" in q or "queue" in q:
        return (
            "### 📚 Stack vs. Queue (Data Structures)\n\n"
            "• **Stack (LIFO - Last In, First Out)**: Like a stack of dinner plates—the last plate placed on top is the first one removed. Operations: `push()`, `pop()`, `peek()`. Used in function call stacks, undo/redo mechanisms, and parentheses matching.\n"
            "• **Queue (FIFO - First In, First Out)**: Like a queue at a movie ticket counter—the first person in line gets served first. Operations: `enqueue()`, `dequeue()`. Used in CPU scheduling, printer task queues, and Breadth-First Search (BFS)."
        )

    if "deadlock" in q:
        return (
            "### 🔒 Deadlock in Operating Systems\n\n"
            "A **Deadlock** occurs when a set of processes are blocked because each process holds a resource and waits for another resource held by another process.\n\n"
            "**The 4 Coffman Conditions for Deadlock**:\n"
            "1. **Mutual Exclusion**: At least one resource cannot be shared.\n"
            "2. **Hold and Wait**: A process holds a resource while waiting for another.\n"
            "3. **No Preemption**: Resources cannot be forcefully taken away.\n"
            "4. **Circular Wait**: A closed chain of processes where each waits for a resource held by the next."
        )

    if "exam" in q or "schedule" in q or "how to study" in q or "prepare" in q:
        return (
            "### 📅 3-Step Exam Preparation Strategy\n\n"
            "1. **Audit the Syllabus**: Identify High-Weightage topics vs. Quick-Win concepts. Spend 60% of your time on core problems that frequently appear in past college papers.\n"
            "2. **Practice Active Problem Solving**: Don't just read code or theory—code it from scratch and trace inputs with pen and paper.\n"
            "3. **Mock Tests & Self-Quizzing**: Use the **AI Quiz Generator** tab to test your recall under timed conditions!"
        )

    # 4. Fallback Encouraging Academic Tutor Response
    return (
        f"### 🤖 StudyMate AI Tutor\n\n"
        f"Great academic question! When studying **{query}**, here is how to master it:\n\n"
        f"1. **Define the Foundation**: Break down the definition into standard terms and identify prerequisites.\n"
        f"2. **Find a Real-World Analogy**: Relate the mechanism to everyday systems (like traffic lights, postal systems, or book catalogs).\n"
        f"3. **Write or Trace Code**: Create a minimal working example to see inputs, transformations, and outputs.\n"
        f"4. **Test Edge Cases**: Always test empty inputs, boundary values, and negative cases.\n\n"
        f"*💡 Tip: Try clicking one of the suggested prompt chips above, or ask me for a code example or quiz question!*"
    )


def get_study_response(user_id, prompt):
    """
    Main interface function for the AI Study Chatbot.
    Tries external API first; if unavailable, uses high-speed local academic engine.
    """
    prompt = prompt.strip()
    if not prompt:
        return "Please ask an academic or study question, and I'll be glad to help!"

    # 1. Try Gemini API if key is present
    gemini_reply = call_gemini_api(prompt)
    if gemini_reply:
        return gemini_reply

    # 2. Try OpenAI API if key is present
    openai_reply = call_openai_api(prompt)
    if openai_reply:
        return openai_reply

    # 3. Use built-in offline Academic Engine
    return generate_local_response(prompt)


# ===================================================================
# AI QUIZ GENERATOR ENGINE (Step 8)
# ===================================================================

QUIZ_BANK = {
    "dsa": [
        {
            "question": "What is the worst-case time complexity of Quick Sort?",
            "options": ["O(n log n)", "O(n)", "O(n²)", "O(log n)"],
            "answer": 2,
            "explanation": "Quick Sort degrades to O(n²) when the chosen pivot is repeatedly the smallest or largest element (such as an already sorted array with naive pivot selection)."
        },
        {
            "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?",
            "options": ["Queue", "Stack", "Binary Heap", "Linked List"],
            "answer": 1,
            "explanation": "A Stack works on the LIFO principle: the last element pushed onto the stack is the first one to be popped."
        },
        {
            "question": "What is the average time complexity to search an element in a balanced Binary Search Tree (BST)?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "answer": 2,
            "explanation": "In a balanced BST, each comparison cuts the search space in half, resulting in an O(log n) time complexity."
        },
        {
            "question": "Which algorithm is used to find the shortest path from a single source vertex in a non-negative weighted graph?",
            "options": ["Prim's Algorithm", "Dijkstra's Algorithm", "Kruskal's Algorithm", "Floyd-Warshall"],
            "answer": 1,
            "explanation": "Dijkstra's algorithm finds the shortest path from a single source to all vertices in graphs with non-negative edge weights."
        },
        {
            "question": "What is the primary advantage of a Doubly Linked List over a Singly Linked List?",
            "options": ["Requires less memory per node", "Can be traversed in both forward and backward directions", "Allows direct random index access", "Guarantees O(1) sorting"],
            "answer": 1,
            "explanation": "Doubly Linked Lists store pointers to both the next and previous nodes, enabling bidirectional traversal."
        }
    ],
    "os": [
        {
            "question": "Which of the following is NOT one of the 4 Coffman conditions required for a Deadlock?",
            "options": ["Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait"],
            "answer": 2,
            "explanation": "The four Coffman conditions are Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. If preemption is allowed, deadlock cannot occur."
        },
        {
            "question": "What is the main difference between a Process and a Thread?",
            "options": ["Processes share memory; threads do not", "Threads of the same process share the same memory space", "A thread cannot be scheduled by the OS", "Processes are always faster to create"],
            "answer": 1,
            "explanation": "Threads share the code and data segments of their parent process, making context switching and communication lightweight."
        },
        {
            "question": "What problem does Paging solve in Operating Systems memory management?",
            "options": ["Internal Fragmentation", "External Fragmentation", "CPU Overheating", "Disk Crash"],
            "answer": 1,
            "explanation": "Paging divides physical memory into fixed-size frames, completely eliminating external fragmentation."
        },
        {
            "question": "Which CPU scheduling algorithm gives CPU time slices equally in a cyclical manner?",
            "options": ["First Come First Serve (FCFS)", "Shortest Job First (SJF)", "Round Robin (RR)", "Priority Scheduling"],
            "answer": 2,
            "explanation": "Round Robin assigns a fixed time quantum to each ready process in circular order, ensuring fairness."
        },
        {
            "question": "What is Virtual Memory?",
            "options": ["A type of high-speed cache memory", "An OS abstraction using secondary storage to simulate larger RAM", "Read-only memory stored on the motherboard", "A virtual reality display module"],
            "answer": 1,
            "explanation": "Virtual Memory allows execution of processes that may not be completely in physical RAM by swapping pages to and from the disk."
        }
    ],
    "dbms": [
        {
            "question": "Which ACID property guarantees that all operations in a database transaction succeed or none take effect?",
            "options": ["Consistency", "Atomicity", "Isolation", "Durability"],
            "answer": 1,
            "explanation": "Atomicity ensures the transaction is treated as an indivisible unit: either all updates are committed, or the transaction rolls back completely."
        },
        {
            "question": "Which Normal Form requires eliminating transitive dependencies (X → Y and Y → Z)?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "answer": 2,
            "explanation": "Third Normal Form (3NF) requires a table to be in 2NF and have no transitive dependencies between non-prime attributes."
        },
        {
            "question": "Which SQL clause is used to filter records after an aggregate function (e.g. GROUP BY)?",
            "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
            "answer": 1,
            "explanation": "The HAVING clause filters aggregated groups, whereas the WHERE clause filters individual rows before grouping."
        },
        {
            "question": "What is the primary purpose of creating a Database Index (B-Tree index)?",
            "options": ["To encrypt sensitive table data", "To speed up data retrieval (SELECT queries)", "To prevent duplicate foreign keys", "To automatically compress table rows"],
            "answer": 1,
            "explanation": "Indexes provide quick lookups (typically O(log n)) without having to perform a full sequential table scan."
        },
        {
            "question": "Which type of JOIN returns all records when there is a match in either left or right table?",
            "options": ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
            "answer": 2,
            "explanation": "FULL OUTER JOIN returns all rows from both tables, filling NULLs where matches are absent."
        }
    ],
    "networks": [
        {
            "question": "How many layers are in the OSI (Open Systems Interconnection) reference model?",
            "options": ["4 layers", "5 layers", "7 layers", "8 layers"],
            "answer": 2,
            "explanation": "The 7 OSI layers are: Physical, Data Link, Network, Transport, Session, Presentation, Application."
        },
        {
            "question": "Which protocol is connectionless and suitable for real-time video streaming or gaming?",
            "options": ["TCP", "UDP", "FTP", "SSH"],
            "answer": 1,
            "explanation": "UDP (User Datagram Protocol) transmits packets without handshakes or delivery guarantees, prioritizing low latency."
        },
        {
            "question": "What does DNS (Domain Name System) do?",
            "options": ["Encrypts web traffic over TLS", "Translates human-readable domain names into IP addresses", "Allocates private IP addresses to local devices", "Detects malicious network packets"],
            "answer": 1,
            "explanation": "DNS works as the phonebook of the Internet, translating names like 'google.com' into IP addresses like '142.250.190.46'."
        },
        {
            "question": "Which HTTP response status code represents 'Page Not Found'?",
            "options": ["200", "301", "404", "500"],
            "answer": 2,
            "explanation": "HTTP 404 indicates that the client was able to communicate with the server, but the requested resource could not be found."
        },
        {
            "question": "What mechanism does TCP use to establish a reliable connection?",
            "options": ["2-Way Ping", "3-Way Handshake (SYN, SYN-ACK, ACK)", "4-Way Checksum", "Dynamic Token Ring"],
            "answer": 1,
            "explanation": "TCP establishes connections through a 3-Way Handshake: Client sends SYN, Server replies SYN-ACK, Client confirms with ACK."
        }
    ],
    "python": [
        {
            "question": "Which of the following built-in Python data types is IMMUTABLE?",
            "options": ["List", "Dictionary", "Set", "Tuple"],
            "answer": 3,
            "explanation": "Tuples are immutable; once instantiated, their elements and length cannot be modified."
        },
        {
            "question": "What is the purpose of the '__init__' method in a Python class?",
            "options": ["To destroy class instances", "To act as the constructor and initialize object attributes", "To import external modules", "To convert objects into JSON strings"],
            "answer": 1,
            "explanation": "The __init__ method is Python's constructor, automatically called when an object is instantiated to set initial attributes."
        },
        {
            "question": "What will 'print(type(5 / 2))' output in Python 3?",
            "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
            "answer": 1,
            "explanation": "In Python 3, the standard division operator '/' always returns a floating-point number (2.5), which has type float."
        },
        {
            "question": "What keyword is used to create a generator function in Python?",
            "options": ["return", "generate", "yield", "produce"],
            "answer": 2,
            "explanation": "The 'yield' keyword pauses function execution and returns a generator iterator value, saving state between calls."
        },
        {
            "question": "Which pillar of Object-Oriented Programming allows a subclass to inherit attributes and methods from a parent class?",
            "options": ["Polymorphism", "Encapsulation", "Abstraction", "Inheritance"],
            "answer": 3,
            "explanation": "Inheritance allows a new class (child) to adopt and reuse the properties and behaviors of an existing class (parent)."
        }
    ]
}


def generate_quiz(topic, difficulty="Medium", num_questions=5):
    """
    Generates a list of multiple-choice questions for the specified topic and difficulty.
    Selects from the curated academic bank or generates structured questions.
    """
    t = topic.lower().strip()
    questions_pool = []

    # Match category
    if "data structure" in t or "dsa" in t or "algorithm" in t or "search" in t or "sort" in t:
        questions_pool = list(QUIZ_BANK["dsa"])
    elif "operating system" in t or "os" in t or "thread" in t or "process" in t or "memory" in t:
        questions_pool = list(QUIZ_BANK["os"])
    elif "database" in t or "dbms" in t or "sql" in t or "acid" in t or "normal" in t:
        questions_pool = list(QUIZ_BANK["dbms"])
    elif "network" in t or "tcp" in t or "ip" in t or "protocol" in t:
        questions_pool = list(QUIZ_BANK["networks"])
    elif "python" in t or "oop" in t or "programming" in t or "code" in t:
        questions_pool = list(QUIZ_BANK["python"])
    else:
        # Combine questions across categories for general / broad topics
        for cat_questions in QUIZ_BANK.values():
            questions_pool.extend(cat_questions)

    # Shuffle to ensure freshness on each attempt
    random.shuffle(questions_pool)

    # Bound question count
    count = min(max(int(num_questions), 1), len(questions_pool))
    selected = questions_pool[:count]

    # Return clean quiz objects
    return selected
