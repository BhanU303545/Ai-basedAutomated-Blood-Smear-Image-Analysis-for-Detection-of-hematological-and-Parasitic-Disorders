const API_BASE = 'http://localhost:5001/api';

export function getCurrentUser() {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
}

export function requireAuth() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = '/index.html';
        return null;
    }
    return user;
}

export async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('currentUser', JSON.stringify(data.user));
            return { success: true, user: data.user };
        } else {
            return { success: false, error: data.error };
        }
    } catch (error) {
        return { success: false, error: 'Network error. Please try again.' };
    }
}

export async function registerUser(userData) {
    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        const data = await response.json();
        
        if (response.ok) {
            return { success: true, user: data.user };
        } else {
            return { success: false, error: data.error };
        }
    } catch (error) {
        return { success: false, error: 'Network error. Please try again.' };
    }
}

export function logoutUser() {
    localStorage.removeItem('currentUser');
    window.location.href = '/index.html';
}

export function updateUserInfo() {
    const user = getCurrentUser();
    console.log('updateUserInfo called, user:', user);
    const userInfoElements = document.querySelectorAll('#userInfo');
    console.log('Found userInfo elements:', userInfoElements.length);
    
    userInfoElements.forEach(element => {
        if (user) {
            const nameElement = element.querySelector('.user-name');
            const roleElement = element.querySelector('.user-role');
            
            console.log('nameElement:', nameElement, 'user.name:', user.name);
            console.log('roleElement:', roleElement, 'user.role:', user.role);
            
            if (nameElement) nameElement.textContent = user.name;
            if (roleElement) roleElement.textContent = user.role;
        }
    });
}

const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const loginMessage = document.getElementById('loginMessage');
const registerMessage = document.getElementById('registerMessage');

const authTabs = document.querySelectorAll('.auth-tab');
if (authTabs.length > 0) {
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            if (targetTab === 'login') {
                loginForm.classList.add('active');
                registerForm.classList.remove('active');
            } else {
                registerForm.classList.add('active');
                loginForm.classList.remove('active');
            }

            loginMessage.classList.remove('error', 'success');
            loginMessage.style.display = 'none';
            registerMessage.classList.remove('error', 'success');
            registerMessage.style.display = 'none';
        });
    });
}

function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `form-message ${type}`;
    element.style.display = 'block';
}

function setLoading(button, isLoading) {
    if (isLoading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        setLoading(loginBtn, true);
        loginMessage.style.display = 'none';

        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const result = await loginUser(email, password);

            if (!result.success) {
                throw new Error(result.error);
            }

            showMessage(loginMessage, 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard.html';
            }, 1000);

        } catch (error) {
            showMessage(loginMessage, error.message || 'Login failed. Please try again.', 'error');
            setLoading(loginBtn, false);
        }
    });
}

if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        setLoading(registerBtn, true);
        registerMessage.style.display = 'none';

        const fullName = document.getElementById('registerName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const role = document.getElementById('registerRole').value;

        if (password.length < 6) {
            showMessage(registerMessage, 'Password must be at least 6 characters long.', 'error');
            setLoading(registerBtn, false);
            return;
        }

        try {
            const result = await registerUser({
                email,
                password,
                name: fullName,
                role
            });

            if (!result.success) {
                throw new Error(result.error);
            }

            const loginResult = await loginUser(email, password);
            if (loginResult.success) {
                showMessage(registerMessage, 'Account created successfully! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard.html';
                }, 1000);
            }

        } catch (error) {
            showMessage(registerMessage, error.message || 'Registration failed. Please try again.', 'error');
            setLoading(registerBtn, false);
        }
    });
}

if (loginForm || registerForm) {
    (async () => {
        const user = getCurrentUser();
        if (user) {
            window.location.href = '/dashboard.html';
        }
    })();
}
