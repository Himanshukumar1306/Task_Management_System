document.addEventListener('DOMContentLoaded', async () => {
    ui.checkAuth();
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (user.role !== 'admin' && user.role !== 'manager') {
        window.location.href = 'dashboard.html';
        return;
    }

    const modal = document.getElementById('employee-modal');
    const openBtn = document.getElementById('open-employee-modal');
    const closeBtn = document.getElementById('close-employee-modal');
    const form = document.getElementById('employee-form');
    const tbody = document.getElementById('employee-list');

    // Display controls based on permissions
    if (user.role === 'admin') {
        if(openBtn) openBtn.style.display = 'inline-flex';
    } else {
        if(openBtn) openBtn.style.display = 'none';
    }

    // Modal behavior
    if (openBtn) {
        openBtn.addEventListener('click', () => { modal.classList.add('active'); });
    }
    if (closeBtn) {
        closeBtn.addEventListener('click', () => { modal.classList.remove('active'); form.reset(); });
    }

    // Load employees list
    async function loadEmployees() {
        try {
            const employees = await api.get('/employees');
            tbody.innerHTML = '';
            
            if (!employees || employees.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 40px;">No employees registered in the system.</td>
                    </tr>
                `;
                return;
            }

            employees.forEach(emp => {
                const tr = document.createElement('tr');
                tr.className = 'fade-in';
                
                const statusBadge = emp.is_active 
                    ? `<span class="badge success">Active</span>` 
                    : `<span class="badge danger">Inactive</span>`;
                
                const actionBtn = (user.role === 'admin' && emp.is_active)
                    ? `<button class="btn-secondary deactivate-btn" data-id="${emp.employee_id}" style="padding: 6px 12px; font-size:12px; border-radius: 6px; line-height: 1;">Deactivate</button>` 
                    : `<span style="color: var(--text-muted); font-size: 13px;">None</span>`;

                tr.innerHTML = `
                    <td style="font-weight: 600;">#${emp.employee_id}</td>
                    <td style="color: var(--text-primary); font-weight: 500;">${emp.full_name}</td>
                    <td>${emp.department || '<span style="color: var(--text-muted)">-</span>'}</td>
                    <td>${emp.designation || '<span style="color: var(--text-muted)">-</span>'}</td>
                    <td>${statusBadge}</td>
                    <td>${actionBtn}</td>
                `;
                tbody.appendChild(tr);
            });

            // Bind deactivate events
            document.querySelectorAll('.deactivate-btn').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const button = e.currentTarget;
                    const id = button.getAttribute('data-id');
                    if (confirm('Are you sure you want to deactivate this employee account?')) {
                        try {
                            button.textContent = '...';
                            button.disabled = true;
                            await api.delete(`/employees/${id}`);
                            ui.showToast('Employee account deactivated');
                            loadEmployees();
                        } catch(err) {
                            button.textContent = 'Deactivate';
                            button.disabled = false;
                        }
                    }
                });
            });
        } catch (error) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: var(--danger); padding: 40px;">Failed to fetch employees list.</td>
                </tr>
            `;
        }
    }

    // Save employee account form handler
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const saveBtn = document.getElementById('save-employee-btn');
            const empData = {
                full_name: document.getElementById('emp-name').value,
                username: document.getElementById('emp-username').value,
                email: document.getElementById('emp-email').value,
                password: document.getElementById('emp-password').value,
                department: document.getElementById('emp-dept').value || null,
                designation: document.getElementById('emp-desig').value || null
            };
            try {
                saveBtn.textContent = 'Creating...';
                saveBtn.disabled = true;
                await api.post('/employees', empData);
                ui.showToast('Employee account created successfully');
                modal.classList.remove('active');
                form.reset();
                loadEmployees();
            } catch (err) {
                // error details displayed via global api.js toast handler
            } finally {
                saveBtn.textContent = 'Create Account';
                saveBtn.disabled = false;
            }
        });
    }

    loadEmployees();
});
