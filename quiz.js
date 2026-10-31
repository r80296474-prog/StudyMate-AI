/**
 * quiz.js - Interactive Client Logic for AI Quiz Generator
 * Manages question flow, interactive selection, score calculation, review breakdown, and SQLite persistence.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Phase Views
    const setupView = document.getElementById('quizSetupView');
    const playerView = document.getElementById('quizPlayerView');
    const resultView = document.getElementById('quizResultView');

    // Controls & Elements
    const quizForm = document.getElementById('quizConfigForm');
    const topicInput = document.getElementById('quizTopicInput');
    const presetPills = document.querySelectorAll('.topic-preset-pill');
    const btnGenerate = document.getElementById('btnGenerateQuiz');

    // Player Elements
    const playerTopic = document.getElementById('playerTopicBadge');
    const playerDifficulty = document.getElementById('playerDifficultyBadge');
    const playerCounter = document.getElementById('playerQuestionCounter');
    const playerProgressFill = document.getElementById('quizProgressFill');
    const questionText = document.getElementById('quizQuestionText');
    const optionsContainer = document.getElementById('quizOptionsContainer');
    const btnNextQuestion = document.getElementById('btnNextQuestion');
    const timerDisplay = document.getElementById('quizTimerDisplay');

    // Result Elements
    const resultScoreText = document.getElementById('resultScoreText');
    const resultPercentBadge = document.getElementById('resultPercentBadge');
    const resultFeedbackBadge = document.getElementById('resultFeedbackBadge');
    const reviewListContainer = document.getElementById('quizReviewList');
    const btnNewQuiz = document.getElementById('btnNewQuiz');

    // Quiz State
    let quizData = [];
    let currentTopic = "";
    let currentDifficulty = "Medium";
    let currentIndex = 0;
    let userAnswers = []; // stores selected option index (0-3) for each question
    let timerInterval = null;
    let secondsElapsed = 0;

    // 1. Preset Topic Buttons
    presetPills.forEach(pill => {
        pill.addEventListener('click', () => {
            presetPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            if (topicInput) {
                topicInput.value = pill.getAttribute('data-topic');
            }
        });
    });

    // 2. Generate Quiz Form Submit
    if (quizForm) {
        quizForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const topic = topicInput.value.trim();
            const difficulty = document.getElementById('quizDifficulty').value;
            const count = document.getElementById('quizCount').value;

            if (!topic) {
                showToast("Please enter or select a study topic.", "warning");
                return;
            }

            // Show loading state
            btnGenerate.disabled = true;
            btnGenerate.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating AI Quiz...';

            try {
                const response = await fetch('/quiz/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        topic: topic,
                        difficulty: difficulty,
                        count: count
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.questions && data.questions.length > 0) {
                        quizData = data.questions;
                        currentTopic = topic;
                        currentDifficulty = difficulty;
                        startQuizPlayer();
                    } else {
                        showToast("Could not generate questions for this topic. Please try another.", "danger");
                    }
                } else {
                    showToast("Server error generating quiz.", "danger");
                }
            } catch (err) {
                console.error("Quiz generation error:", err);
                showToast("Network error. Please try again.", "danger");
            } finally {
                btnGenerate.disabled = false;
                btnGenerate.innerHTML = '<i class="fa-solid fa-bolt"></i> Generate Practice Quiz';
            }
        });
    }

    // 3. Start Quiz Player
    function startQuizPlayer() {
        currentIndex = 0;
        userAnswers = new Array(quizData.length).fill(null);
        secondsElapsed = 0;

        // Update Header Badges
        if (playerTopic) playerTopic.textContent = currentTopic;
        if (playerDifficulty) playerDifficulty.textContent = currentDifficulty;

        // Switch View
        setupView.style.display = 'none';
        resultView.style.display = 'none';
        playerView.style.display = 'block';

        // Start Timer
        startTimer();

        // Render First Question
        renderQuestion(currentIndex);
    }

    function startTimer() {
        clearInterval(timerInterval);
        secondsElapsed = 0;
        timerInterval = setInterval(() => {
            secondsElapsed++;
            const mins = String(Math.floor(secondsElapsed / 60)).padStart(2, '0');
            const secs = String(secondsElapsed % 60).padStart(2, '0');
            if (timerDisplay) timerDisplay.textContent = `${mins}:${secs}`;
        }, 1000);
    }

    // 4. Render Active Question
    function renderQuestion(index) {
        const q = quizData[index];
        const total = quizData.length;

        // Update progress counters
        playerCounter.textContent = `Question ${index + 1} of ${total}`;
        const percent = Math.round(((index + 1) / total) * 100);
        playerProgressFill.style.width = `${percent}%`;

        // Render question text
        questionText.textContent = q.question;

        // Render options (A, B, C, D)
        const letters = ['A', 'B', 'C', 'D'];
        optionsContainer.innerHTML = '';

        q.options.forEach((optText, optIdx) => {
            const optCard = document.createElement('div');
            optCard.className = 'quiz-option';
            if (userAnswers[index] === optIdx) {
                optCard.classList.add('selected');
            }

            optCard.innerHTML = `
                <div class="option-badge">${letters[optIdx]}</div>
                <div class="option-label">${escapeHtml(optText)}</div>
            `;

            optCard.addEventListener('click', () => {
                // Select option
                document.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
                optCard.classList.add('selected');
                userAnswers[index] = optIdx;
                btnNextQuestion.disabled = false;
            });

            optionsContainer.appendChild(optCard);
        });

        // Set button label
        if (index === total - 1) {
            btnNextQuestion.innerHTML = '<span>Submit Test & View Score</span> <i class="fa-solid fa-flag-checkered"></i>';
        } else {
            btnNextQuestion.innerHTML = '<span>Next Question</span> <i class="fa-solid fa-arrow-right"></i>';
        }

        // Disable next button until selection is made
        btnNextQuestion.disabled = (userAnswers[index] === null);
    }

    // 5. Next Question / Submit Handler
    if (btnNextQuestion) {
        btnNextQuestion.addEventListener('click', () => {
            if (userAnswers[currentIndex] === null) {
                showToast("Please choose an option before proceeding.", "warning");
                return;
            }

            if (currentIndex < quizData.length - 1) {
                currentIndex++;
                renderQuestion(currentIndex);
            } else {
                finishQuiz();
            }
        });
    }

    // 6. Finish Quiz & Calculate Score
    async function finishQuiz() {
        clearInterval(timerInterval);

        let score = 0;
        const total = quizData.length;

        quizData.forEach((q, idx) => {
            if (userAnswers[idx] === q.answer) {
                score++;
            }
        });

        const percentage = Math.round((score / total) * 100);

        // Display results UI
        resultScoreText.textContent = `${score}/${total}`;
        resultPercentBadge.textContent = `${percentage}%`;

        if (percentage >= 80) {
            resultFeedbackBadge.className = 'badge badge-low';
            resultFeedbackBadge.textContent = '🎉 Outstanding Performance!';
        } else if (percentage >= 50) {
            resultFeedbackBadge.className = 'badge badge-medium';
            resultFeedbackBadge.textContent = '👍 Good Effort! Keep Revising';
        } else {
            resultFeedbackBadge.className = 'badge badge-high';
            resultFeedbackBadge.textContent = '📚 Needs Practice & Revision';
        }

        // Render Detailed Review Breakdown
        renderReviewBreakdown();

        // Switch to Result View
        playerView.style.display = 'none';
        resultView.style.display = 'block';

        // Save Attempt to SQLite Backend
        try {
            await fetch('/quiz/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    topic: currentTopic,
                    difficulty: currentDifficulty,
                    score: score,
                    total_questions: total
                })
            });
            showToast("Quiz result saved to your study record! 🏆", "success");
        } catch (err) {
            console.error("Save quiz error:", err);
        }
    }

    // 7. Render Review Breakdown
    function renderReviewBreakdown() {
        reviewListContainer.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D'];

        quizData.forEach((q, idx) => {
            const userChoice = userAnswers[idx];
            const isCorrect = (userChoice === q.answer);

            const reviewCard = document.createElement('div');
            reviewCard.className = `review-item ${isCorrect ? 'correct' : 'incorrect'}`;

            const userChoiceText = userChoice !== null ? `${letters[userChoice]}: ${q.options[userChoice]}` : 'No Answer Selected';
            const correctChoiceText = `${letters[q.answer]}: ${q.options[q.answer]}`;

            reviewCard.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <h4 style="font-size: 1rem; color: var(--text-main);">Question ${idx + 1}: ${escapeHtml(q.question)}</h4>
                    <span class="badge ${isCorrect ? 'badge-low' : 'badge-high'}">
                        ${isCorrect ? '<i class="fa-solid fa-check"></i> Correct' : '<i class="fa-solid fa-xmark"></i> Incorrect'}
                    </span>
                </div>
                <div style="font-size: 0.88rem; margin-bottom: 6px;">
                    <span style="color: var(--text-muted);">Your Answer:</span> 
                    <strong style="color: ${isCorrect ? 'var(--status-success)' : 'var(--status-danger)'};">${escapeHtml(userChoiceText)}</strong>
                </div>
                ${!isCorrect ? `
                    <div style="font-size: 0.88rem; margin-bottom: 6px;">
                        <span style="color: var(--text-muted);">Correct Answer:</span> 
                        <strong style="color: var(--status-success);">${escapeHtml(correctChoiceText)}</strong>
                    </div>
                ` : ''}
                <div class="review-explanation">
                    <strong>💡 Concept Explanation:</strong> ${escapeHtml(q.explanation)}
                </div>
            `;

            reviewListContainer.appendChild(reviewCard);
        });
    }

    // 8. Retake / New Quiz Button
    if (btnNewQuiz) {
        btnNewQuiz.addEventListener('click', () => {
            resultView.style.display = 'none';
            playerView.style.display = 'none';
            setupView.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
