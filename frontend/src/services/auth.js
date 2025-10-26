import api from "./api"

export const registerUser = (userData) => api.post('user/create/', userData);
export const loginUser = (credentials) => api.post('user/token', credentials);
export const getCurrentUser = (token) =>
    api.get('user/me/', {
        headers: {
            Authorization: `Bearer ${token}`,

        },
    });