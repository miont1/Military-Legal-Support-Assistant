import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
});

// Add a request interceptor to include the auth token if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

export const sendMessage = async (question, metadata = {}, sessionId = null) => {
    try {
        const payload = { question, ...metadata };
        if (sessionId) {
            payload.session_id = sessionId;
        }
        const response = await api.post('/chat/', payload);
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};

export const getSessions = async () => {
    try {
        const response = await api.get('/sessions/');
        return response.data;
    } catch (error) {
        console.error("Get Sessions Error:", error);
        return [];
    }
};

export const getSessionMessages = async (sessionId) => {
    try {
        const response = await api.get(`/sessions/${sessionId}/`);
        return response.data;
    } catch (error) {
        console.error("Get Messages Error:", error);
        return [];
    }
};

export const deleteSession = async (sessionId) => {
    try {
        await api.delete(`/sessions/${sessionId}/`);
        return true;
    } catch (error) {
        console.error("Delete Session Error:", error);
        return false;
    }
};

export const getUserProfile = async () => {
    try {
        const response = await api.get('/profile/');
        return response.data;
    } catch (error) {
        console.error("Get Profile Error:", error);
        throw error;
    }
};

export const updateUserProfile = async (data) => {
    try {
        const response = await api.patch('/profile/', data);
        return response.data;
    } catch (error) {
        console.error("Update Profile Error:", error);
        throw error;
    }
};

export const changePassword = async (data) => {
    try {
        const response = await api.post('/change-password/', data);
        return response.data;
    } catch (error) {
        console.error("Change Password Error:", error);
        throw error;
    }
};

export const registerUser = async (userData) => {
    try {
        const response = await api.post('/register/', userData);
        return response.data;
    } catch (error) {
        console.error("Registration Error:", error);
        throw error;
    }
};

export const loginUser = async (credentials) => {
    try {
        const response = await api.post('/login/', credentials);
        return response.data;
    } catch (error) {
        console.error("Login Error:", error);
        throw error;
    }
};

export default api;
