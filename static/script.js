document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutBtn = document.getElementById('logout-btn');
    const message = document.getElementById('message');
    const usernameSpan = document.getElementById('username');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const res = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();
            if (res.ok) {
                window.location.href = '/profile';
            } else {
                message.textContent = data.message;
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const res = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();
            if (res.ok) {
                window.location.href = '/login';
            } else {
                message.textContent = data.message;
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            const res = await fetch('/api/logout');
            if (res.ok) {
                window.location.href = '/';
            }
        });
    }

    if (usernameSpan) {
        fetch('/api/profile')
            .then(res => res.json())
            .then(data => {
                if (data.username) {
                    usernameSpan.textContent = data.username;
                } else {
                    window.location.href = '/login';
                }
            });
    }
});
