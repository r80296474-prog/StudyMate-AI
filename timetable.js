/**
 * timetable.js - Interactive Client Logic for Tasks & Weekly Timetable
 * Handles real-time filtering, AJAX task toggling, and modal windows.
 */

// Modal Helper Functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// Close modal when clicking on the backdrop
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('open');
                document.body.style.overflow = '';
            }
        });
    });

    // Task Filter Handling
    const filterPills = document.querySelectorAll('.filter-pill');
    const taskItems = document.querySelectorAll('.task-item');

    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const filter = pill.getAttribute('data-filter');

            taskItems.forEach(item => {
                const isCompleted = item.classList.contains('completed');
                const priority = item.getAttribute('data-priority');

                if (filter === 'all') {
                    item.style.display = 'flex';
                } else if (filter === 'pending') {
                    item.style.display = !isCompleted ? 'flex' : 'none';
                } else if (filter === 'completed') {
                    item.style.display = isCompleted ? 'flex' : 'none';
                } else if (filter === 'high' || filter === 'medium' || filter === 'low') {
                    item.style.display = (priority && priority.toLowerCase() === filter) ? 'flex' : 'none';
                }
            });
        });
    });
});

/**
 * Toggle Task Completion via Fetch API (AJAX)
 * @param {number} taskId 
 * @param {HTMLElement} btnElement 
 */
async function toggleTaskStatus(taskId, btnElement) {
    try {
        const response = await fetch(`/tasks/${taskId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const data = await response.json();
            const taskItem = document.getElementById(`task-item-${taskId}`);

            if (data.is_completed) {
                btnElement.classList.add('checked');
                btnElement.innerHTML = '<i class="fa-solid fa-check"></i>';
                if (taskItem) taskItem.classList.add('completed');
                showToast('Task marked as completed! 🎉', 'success');
            } else {
                btnElement.classList.remove('checked');
                btnElement.innerHTML = '';
                if (taskItem) taskItem.classList.remove('completed');
                showToast('Task moved back to pending.', 'info');
            }

            // Update progress bar and counters if present on the page
            updateTaskProgressUI(data.total_tasks, data.completed_tasks, data.progress_percent);
        } else {
            showToast('Failed to update task status.', 'danger');
        }
    } catch (err) {
        console.error('Task toggle error:', err);
        // Fallback: submit standard form if AJAX fails
        const fallbackForm = document.getElementById(`form-toggle-${taskId}`);
        if (fallbackForm) fallbackForm.submit();
    }
}

/**
 * Updates task progress bar and text counters dynamically
 */
function updateTaskProgressUI(total, completed, percent) {
    const fill = document.getElementById('taskProgressFill');
    const label = document.getElementById('taskProgressLabel');
    const badge = document.getElementById('taskProgressBadge');

    if (fill) fill.style.width = `${percent}%`;
    if (label) label.textContent = `${completed} of ${total} tasks completed (${percent}%)`;
    if (badge) badge.textContent = `${percent}%`;
}
