// Change this URL to your actual backend URL after deploying the backend to Render!
const RENDER_BACKEND_URL = 'https://task-management-system-1-4kof.onrender.com';

const BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api/v1'
    : `${RENDER_BACKEND_URL}/api/v1`;

const api = {
    request: async (endpoint, options = {}) => {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${BASE_URL}${endpoint}`, {
                ...options,
                headers
            });

            // If 401 Unauthorized, redirect to login page (unless already on landing/login)
            const isAuthPage = window.location.pathname.endsWith('/index.html') || 
                               window.location.pathname.endsWith('/login.html') || 
                               window.location.pathname === '/' || 
                               window.location.pathname === '';
                               
            if (response.status === 401 && !isAuthPage) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = 'login.html';
                return null;
            }

            if (response.status === 204) {
                return true;
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }

            return data;
        } catch (error) {
            ui.showToast(error.message, 'error');
            throw error;
        }
    },

    get: (endpoint) => api.request(endpoint),
    post: (endpoint, body) => api.request(endpoint, { method: 'POST', body: JSON.stringify(body) }),
    put: (endpoint, body) => api.request(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
    patch: (endpoint, body) => api.request(endpoint, { method: 'PATCH', body: JSON.stringify(body) }),
    delete: (endpoint) => api.request(endpoint, { method: 'DELETE' })
};

const ui = {
    showToast: (message, type = 'success') => {
        const container = document.getElementById('toast-container');
        if (!container) return;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
    
    checkAuth: () => {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        
        const isAuthPage = window.location.pathname.endsWith('/index.html') || 
                           window.location.pathname.endsWith('/login.html') || 
                           window.location.pathname === '/' || 
                           window.location.pathname === '';
                           
        if (!token && !isAuthPage) {
            window.location.href = 'login.html';
            return;
        }

        if (user.role === 'admin' || user.role === 'manager') {
            const empNav = document.getElementById('nav-employees');
            if (empNav) empNav.style.display = 'flex'; // Use flex to match upgraded navigation styles
            
            const btnNewTask = document.getElementById('open-task-modal');
            if(btnNewTask) btnNewTask.style.display = 'inline-flex';
        }

        const nameEl = document.getElementById('current-user-name');
        if (nameEl && user.username) {
            nameEl.textContent = `${user.username} (${user.role})`;
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            ui.logout();
        });
    }
});
