
document.addEventListener('DOMContentLoaded', () => {
    // If already logged in, redirect to dashboard
    if (localStorage.getItem('token')) {
        window.location.href = 'dashboard.html';
    }

    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const btn = document.getElementById('login-btn');
            
            try {
                btn.textContent = 'Signing In...';
                btn.disabled = true;
                
                const data = await api.post('/auth/login', { username, password });
                
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', JSON.stringify({
                    user_id: data.user_id,
                    role: data.role,
                    username: username
                }));
                
                ui.showToast('Login successful!');
                
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 500);
            } catch (error) {
                // error handled by api request catch block
            } finally {
                btn.textContent = 'Sign In';
                btn.disabled = false;
            }
        });
    }
});

