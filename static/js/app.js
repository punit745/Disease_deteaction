/* ========================================
   NeuroScan - Main JavaScript
======================================== */

// API Base URL
const API_URL = window.location.origin;

// Token management
function getToken() {
    return localStorage.getItem('neuroToken');
}

function setToken(token) {
    localStorage.setItem('neuroToken', token);
}

function clearToken() {
    localStorage.removeItem('neuroToken');
    localStorage.removeItem('neuroUser');
}

function getUser() {
    const user = localStorage.getItem('neuroUser');
    return user ? JSON.parse(user) : null;
}

function setUser(user) {
    localStorage.setItem('neuroUser', JSON.stringify(user));
}

// Check authentication status on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});

function checkAuth() {
    const token = getToken();
    const user = getUser();
    
    if (token && user) {
        // User is logged in
        const authButtons = document.getElementById('auth-buttons');
        const userMenu = document.getElementById('user-menu');
        const userName = document.getElementById('user-name');
        
        if (authButtons) authButtons.style.display = 'none';
        if (userMenu) {
            userMenu.style.display = 'flex';
            if (userName) userName.textContent = user.first_name;
        }
    }
}

// Modal functions
function showModal(modalId) {
    document.getElementById(modalId).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function hideModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    document.body.style.overflow = '';
    // Clear errors
    const errorEl = document.querySelector(`#${modalId} .form-error`);
    if (errorEl) errorEl.textContent = '';
}

function switchModal(fromId, toId) {
    hideModal(fromId);
    setTimeout(() => showModal(toId), 200);
}

// Scroll function
function scrollTo(elementId) {
    document.getElementById(elementId).scrollIntoView({ behavior: 'smooth' });
}

// Login handler
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');
    
    try {
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            setToken(data.token);
            setUser(data.user);
            hideModal('loginModal');
            window.location.href = '/dashboard';
        } else {
            errorEl.textContent = data.message || 'Login failed';
        }
    } catch (error) {
        errorEl.textContent = 'Connection error. Please try again.';
        console.error('Login error:', error);
    }
}

// Register handler
async function handleRegister(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorEl = document.getElementById('registerError');
    
    try {
        const response = await fetch(`${API_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                first_name: firstName,
                last_name: lastName
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Auto-login after registration
            await handleAutoLogin(email, password);
        } else {
            errorEl.textContent = data.message || 'Registration failed';
        }
    } catch (error) {
        errorEl.textContent = 'Connection error. Please try again.';
        console.error('Registration error:', error);
    }
}

async function handleAutoLogin(email, password) {
    try {
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            setToken(data.token);
            setUser(data.user);
            window.location.href = '/dashboard';
        }
    } catch (error) {
        console.error('Auto-login error:', error);
        window.location.href = '/dashboard';
    }
}

// Logout handler
function logout() {
    clearToken();
    window.location.href = '/';
}

// Go to dashboard
function goToDashboard() {
    window.location.href = '/dashboard';
}

// API helper function
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        // Token expired or invalid
        clearToken();
        window.location.href = '/';
        return null;
    }
    
    return response;
}
