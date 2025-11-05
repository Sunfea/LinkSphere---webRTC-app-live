// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// ========================
// Utility Functions
// ========================

function getAuthToken() {
    return localStorage.getItem('authToken');
}

function setAuthToken(token) {
    localStorage.setItem('authToken', token);
}

function removeAuthToken() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('assignedUsername');
}

function getUsernameFromToken() {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub || payload.username;
    } catch (e) {
        console.error('Failed to parse token:', e);
        return null;
    }
}

function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = `form-message ${isError ? 'error' : 'success'}`;
        element.style.display = 'block';
    }
}

function clearMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

function setButtonLoading(buttonId, isLoading, originalText = '') {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = isLoading;
        if (isLoading) {
            button.setAttribute('data-original-text', button.textContent);
            button.textContent = 'Loading...';
        } else {
            button.textContent = button.getAttribute('data-original-text') || originalText;
        }
    }
}

// ========================
// API Calls
// ========================

async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getAuthToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// ========================
// Authentication Handlers
// ========================

async function handleSignup(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Clear previous errors
    clearMessage('formMessage');
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    document.getElementById('confirmPasswordError').textContent = '';
    
    // Validation
    if (!email || !password || !confirmPassword) {
        showMessage('formMessage', 'Please fill in all fields', true);
        return;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('confirmPasswordError').textContent = 'Passwords do not match';
        return;
    }
    
    if (password.length < 8) {
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters';
        return;
    }
    
    setButtonLoading('signupBtn', true);
    
    try {
        const data = await apiCall('/api/auth/register', {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ email, password })
        });
        
        // Store email and password for verification page
        localStorage.setItem('pendingEmail', email);
        localStorage.setItem('pendingPassword', password);
        
        showMessage('formMessage', 'Account created! Redirecting to verification...', false);
        
        setTimeout(() => {
            window.location.href = '/verify';
        }, 1500);
        
    } catch (error) {
        showMessage('formMessage', error.message || 'Signup failed', true);
        setButtonLoading('signupBtn', false);
    }
}

async function handleVerifyOTP(event) {
    event.preventDefault();
    
    const otp = document.getElementById('otp').value.trim();
    const email = localStorage.getItem('pendingEmail');
    
    clearMessage('formMessage');
    document.getElementById('otpError').textContent = '';
    
    if (!email) {
        showMessage('formMessage', 'No pending verification. Please sign up first.', true);
        setTimeout(() => window.location.href = '/signup', 2000);
        return;
    }
    
    if (!otp || otp.length !== 6) {
        document.getElementById('otpError').textContent = 'Please enter a valid 6-digit OTP';
        return;
    }
    
    setButtonLoading('verifyBtn', true);
    
    try {
        const data = await apiCall('/api/auth/verify-otp', {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ email, otp })
        });
        
        // Extract username from message (format: "Email verified successfully. Your username is: username")
        const username = data.message.split('Your username is: ')[1];
        
        // Store username for display
        localStorage.setItem('assignedUsername', username);
        
        showMessage('formMessage', 'Email verified! Redirecting...', false);
        
        setTimeout(() => {
            window.location.href = '/username';
        }, 1500);
        
    } catch (error) {
        showMessage('formMessage', error.message || 'Verification failed', true);
        setButtonLoading('verifyBtn', false);
    }
}

async function handleResendOTP(event) {
    event.preventDefault();
    
    const email = localStorage.getItem('pendingEmail');
    
    if (!email) {
        showMessage('formMessage', 'No pending verification', true);
        return;
    }
    
    clearMessage('formMessage');
    
    try {
        const password = localStorage.getItem('pendingPassword');
        
        // Call register again to resend OTP
        await apiCall('/api/auth/register', {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ email, password })
        });
        
        showMessage('formMessage', 'New OTP sent to your email!', false);
        
    } catch (error) {
        showMessage('formMessage', 'Failed to resend OTP. Please try signing up again.', true);
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    clearMessage('formMessage');
    document.getElementById('usernameError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    
    if (!username || !password) {
        showMessage('formMessage', 'Please fill in all fields', true);
        return;
    }
    
    setButtonLoading('loginBtn', true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        // Store token and username
        setAuthToken(data.access_token);
        localStorage.setItem('assignedUsername', data.username);
        
        showMessage('formMessage', 'Login successful! Redirecting...', false);
        
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 1000);
        
    } catch (error) {
        showMessage('formMessage', error.message || 'Login failed', true);
        setButtonLoading('loginBtn', false);
    }
}

function handleLogout() {
    removeAuthToken();
    window.location.href = '/login';
}

// ========================
// Auth Guard
// ========================

function requireAuth() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}
