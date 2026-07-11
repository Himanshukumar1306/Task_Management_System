
document.addEventListener('DOMContentLoaded', async () => {
    ui.checkAuth();

    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.role === 'admin' || user.role === 'manager') {
        try {
            const summary = await api.get('/dashboard/summary');
            document.getElementById('stat-total').textContent = summary.total_tasks;
            document.getElementById('stat-completed').textContent = summary.completed;
            document.getElementById('stat-inprogress').textContent = summary.in_progress;
            document.getElementById('stat-pending').textContent = summary.pending;
            document.getElementById('stat-overdue').textContent = summary.overdue;
        } catch (error) {
            console.error('Failed to fetch dashboard summary', error);
        }
    } else {
        // Employees don't have access to global summary
        document.querySelector('.summary-cards').style.display = 'none';
    }

    // Fetch recent tasks
    try {
        const tasks = await api.get('/tasks?limit=5');
        const taskList = document.getElementById('recent-tasks-list');
        taskList.innerHTML = '';
        
        if (tasks.length === 0) {
            taskList.innerHTML = '<p>No recent tasks found.</p>';
            return;
        }
        
        tasks.forEach(task => {
            const div = document.createElement('div');
            div.style.padding = '12px';
            div.style.borderBottom = '1px solid var(--border-color)';
            
            const badgeClass = {
                'Pending': 'pending',
                'In Progress': 'warning',
                'Completed': 'success',
                'Overdue': 'danger'
            }[task.status] || 'pending';

            div.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>${task.title}</strong>
                    <span class="badge ${badgeClass}">${task.status}</span>
                </div>
                <small style="color:var(--text-secondary)">Due: ${task.due_date || 'N/A'} - Priority: ${task.priority}</small>
            `;
            taskList.appendChild(div);
        });
    } catch (error) {
        console.error('Failed to load recent tasks', error);
    }
});

