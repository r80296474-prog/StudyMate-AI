/**
 * chat.js - Interactive Client Logic for AI Study Tutor (Chatbot)
 * Handles real-time messaging, typing animations, markdown parsing, and prompt chips.
 */

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const messagesContainer = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    const promptChips = document.querySelectorAll('.prompt-chip');
    const btnClearChat = document.getElementById('btnClearChat');

    // Auto-scroll to bottom of chat history on initial page load
    scrollToBottom();

    // 1. Submit Question to AI Tutor
    if (chatForm && chatInput) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Display user message in UI immediately
            appendUserMessage(message);
            chatInput.value = '';
            chatInput.focus();

            // Show typing indicator
            showTyping(true);

            try {
                const response = await fetch('/chatbot/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ message: message })
                });

                showTyping(false);

                if (response.ok) {
                    const data = await response.json();
                    appendAiMessage(data.reply, data.timestamp);
                } else {
                    appendAiMessage("I'm sorry, an error occurred while processing your question. Please try asking again!");
                }
            } catch (err) {
                console.error("Chat error:", err);
                showTyping(false);
                appendAiMessage("Network error: Could not connect to the study assistant. Please check your connection.");
            }
        });
    }

    // 2. Clickable Prompt Chips
    promptChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt');
            if (chatInput && promptText) {
                chatInput.value = promptText;
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    });

    // 3. Clear Chat History
    if (btnClearChat) {
        btnClearChat.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to clear your study chat history?')) return;
            try {
                const res = await fetch('/chatbot/clear', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                if (res.ok) {
                    // Remove all message rows except welcome greeting
                    const rows = messagesContainer.querySelectorAll('.message-row');
                    rows.forEach(r => r.remove());
                    showToast('Chat history cleared successfully.', 'info');
                    // Add fresh welcome message
                    appendAiMessage("Chat history cleared! What academic concept would you like to explore today? 🚀");
                }
            } catch (err) {
                console.error("Clear chat error:", err);
            }
        });
    }

    function showTyping(show) {
        if (typingIndicator) {
            typingIndicator.style.display = show ? 'flex' : 'none';
            if (show) scrollToBottom();
        }
    }

    function scrollToBottom() {
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    function appendUserMessage(text) {
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const row = document.createElement('div');
        row.className = 'message-row user-row';
        row.innerHTML = `
            <div class="msg-avatar user">
                <i class="fa-solid fa-user"></i>
            </div>
            <div class="msg-bubble">
                <div class="msg-text">${escapeHtml(text)}</div>
                <span class="msg-time">${timeStr}</span>
            </div>
        `;
        messagesContainer.appendChild(row);
        scrollToBottom();
    }

    function appendAiMessage(rawMarkdown, timestamp) {
        const timeStr = timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const formattedHtml = parseMarkdownToHtml(rawMarkdown);

        const row = document.createElement('div');
        row.className = 'message-row ai-row';
        row.innerHTML = `
            <div class="msg-avatar ai">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="msg-bubble">
                <div class="msg-text">${formattedHtml}</div>
                <span class="msg-time">${timeStr}</span>
            </div>
        `;
        messagesContainer.appendChild(row);
        scrollToBottom();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Converts basic markdown (headers, bold, code blocks, lists) into safe HTML
     */
    function parseMarkdownToHtml(md) {
        if (!md) return '';

        // 1. Code blocks: ```language ... ```
        let html = md.replace(/```(?:python|java|cpp|c|sql|javascript)?\n([\s\S]*?)```/g, (match, code) => {
            return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
        });

        // 2. Inline code: `code`
        html = html.replace(/`([^`]+)`/g, (match, inline) => {
            return `<code>${escapeHtml(inline)}</code>`;
        });

        // 3. Headers: ### Header
        html = html.replace(/^### (.*$)/gim, '<h4 style="font-size: 1.1rem; margin: 10px 0 6px; color: var(--accent-cyan);">$1</h4>');
        html = html.replace(/^## (.*$)/gim, '<h3 style="font-size: 1.2rem; margin: 12px 0 6px; color: var(--accent-cyan);">$1</h3>');

        // 4. Bold: **text**
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // 5. Italic: *text*
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // 6. Bullet points: • or -
        html = html.replace(/^[•\-] (.*$)/gim, '<li style="margin-left: 20px; margin-bottom: 4px;">$1</li>');

        // 7. Line breaks
        html = html.replace(/\n\n/g, '<br><br>');
        html = html.replace(/\n/g, '<br>');

        return html;
    }
});
