document.addEventListener('DOMContentLoaded', async () => {
    ui.checkAuth();
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    const taskGrid = document.getElementById('task-list');
    const modal = document.getElementById('task-modal');
    const openBtn = document.getElementById('open-task-modal');
    const closeBtn = document.getElementById('close-task-modal');
    const form = document.getElementById('task-form');
    const filterBtn = document.getElementById('apply-filters');
    const filterAssignee = document.getElementById('filter-assignee');
    const filterStatus = document.getElementById('filter-status');
    const assigneeSelect = document.getElementById('task-assignee');

    let employeesMap = {}; // id -> name

    // Load setup data if admin/manager
    if (user.role === 'admin' || user.role === 'manager') {
        if(openBtn) openBtn.style.display = 'inline-flex';
        if(filterAssignee) filterAssignee.style.display = 'inline-block';
        
        // Fetch employees for dropdowns
        try {
            const employees = await api.get('/employees');
            employees.forEach(emp => {
                employeesMap[emp.employee_id] = emp.full_name;
                
                const optFilter = document.createElement('option');
                optFilter.value = emp.employee_id;
                optFilter.textContent = emp.full_name;
                filterAssignee.appendChild(optFilter);

                const optForm = document.createElement('option');
                optForm.value = emp.employee_id;
                optForm.textContent = emp.full_name;
                assigneeSelect.appendChild(optForm);
            });
        } catch(err){}
    }

    // Modal behavior
    if(openBtn) openBtn.addEventListener('click', () => { modal.classList.add('active'); });
    if(closeBtn) closeBtn.addEventListener('click', () => { modal.classList.remove('active'); form.reset(); });

    // Load tasks
    async function loadTasks() {
        try {
            let url = '/tasks?limit=100';
            const status = filterStatus.value;
            const assignee = filterAssignee.value;
            
            if (status) url += `&status=${status}`;
            if (assignee && user.role !== 'employee') url += `&assigned_to=${assignee}`;

            const tasks = await api.get(url);
            taskGrid.innerHTML = '';
            
            if (!tasks || tasks.length === 0) {
                taskGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px 0;">No tasks found.</p>';
                return;
            }

            tasks.forEach(task => {
                const card = document.createElement('div');
                card.className = 'task-card fade-in';
                
                const badgeClass = {
                    'Pending': 'pending',
                    'In Progress': 'warning',
                    'Completed': 'success',
                    'Overdue': 'danger'
                }[task.status] || 'pending';

                const assigneeName = employeesMap[task.assigned_to] || `ID: ${task.assigned_to}`;

                let statusActions = '';
                if (user.role === 'employee' || user.role === 'admin' || user.role === 'manager') {
                    // Everyone can update status
                    statusActions = `
                        <div style="margin-top:20px; display:flex; gap:8px; align-items:center; border-top: 1px solid var(--surface-border); padding-top:16px;">
                            <select class="status-update-select" data-id="${task.task_id}" style="padding:8px 12px; font-size:13px; background: rgba(0,0,0,0.3); border:1px solid var(--surface-border); color:white; border-radius:8px; flex: 1; outline:none;">
                                <option value="Pending" ${task.status==='Pending'?'selected':''}>Pending</option>
                                <option value="In Progress" ${task.status==='In Progress'?'selected':''}>In Progress</option>
                                <option value="Completed" ${task.status==='Completed'?'selected':''}>Completed</option>
                            </select>
                            <button class="btn-primary update-status-btn" data-id="${task.task_id}" style="padding:8px 14px; font-size:13px; width:auto; border-radius:8px; line-height: 1.2;">Update</button>
                        </div>
                    `;
                }

                // Render task priority badge
                const priorityColor = {
                    'Low': 'var(--secondary)',
                    'Medium': 'var(--warning)',
                    'High': 'var(--danger)'
                }[task.priority] || 'var(--text-secondary)';

                card.innerHTML = `
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                        <span class="badge ${badgeClass}">${task.status}</span>
                        <span style="font-size:12px; font-weight:700; color:${priorityColor}; text-transform:uppercase; letter-spacing:0.05em;">${task.priority} Priority</span>
                    </div>
                    <h4>${task.title}</h4>
                    <p>${task.description || 'No description provided.'}</p>
                    
                    <div class="task-meta">
                        <div class="task-meta-row">
                            <span class="task-meta-label">Assigned To</span>
                            <span class="task-meta-value">${assigneeName}</span>
                        </div>
                        <div class="task-meta-row">
                            <span class="task-meta-label">Due Date</span>
                            <span class="task-meta-value" style="color: ${task.status==='Overdue'?'var(--danger)':'var(--text-secondary)'}">${task.due_date || 'No Date'}</span>
                        </div>
                    </div>
                    ${statusActions}
                `;
                taskGrid.appendChild(card);
            });

            // Bind status update events
            document.querySelectorAll('.update-status-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const button = e.currentTarget;
                    const id = button.getAttribute('data-id');
                    const select = document.querySelector(`.status-update-select[data-id="${id}"]`);
                    const newStatus = select.value;
                    const isCompleted = newStatus === 'Completed';

                    try {
                        button.textContent = '...';
                        button.disabled = true;
                        await api.patch(`/tasks/${id}/status`, { status: newStatus, completed: isCompleted });
                        ui.showToast('Task status updated successfully');
                        loadTasks();
                    } catch(err) {
                        button.textContent = 'Update';
                        button.disabled = false;
                    }
                });
            });

        } catch (error) {}
    }

    // Form submit to create a task
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const saveBtn = document.getElementById('save-task-btn');
            const data = {
                title: document.getElementById('task-title').value,
                description: document.getElementById('task-desc').value || null,
                assigned_to: parseInt(document.getElementById('task-assignee').value),
                priority: document.getElementById('task-priority').value,
                due_date: document.getElementById('task-due').value || null
            };
            try {
                saveBtn.textContent = 'Saving...';
                saveBtn.disabled = true;
                await api.post('/tasks', data);
                ui.showToast('Task created successfully');
                modal.classList.remove('active');
                form.reset();
                loadTasks();
            } catch(err) {
                // error is reported via toast by the api module
            } finally {
                saveBtn.textContent = 'Save Task';
                saveBtn.disabled = false;
            }
        });
    }

    if(filterBtn) {
        filterBtn.addEventListener('click', loadTasks);
    }

    // Initial load
    loadTasks();
});
