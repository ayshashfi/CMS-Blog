import axios from 'axios';
import { refreshAccessToken, saveTokens } from './auth'; // Import the refresh logic

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Your backend API URL
});

// Add the Authorization header to all requests
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401 error (token expired)
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refresh');

    if (error.response.status === 401 && refreshToken) {
      try {
        const newAccessToken = await refreshAccessToken(refreshToken); // Refresh the token
        if (newAccessToken) {
          saveTokens(newAccessToken, refreshToken); // Save the new access token
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`; // Set new token in the request header
          return axiosInstance(originalRequest); // Retry the original request with the new token
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        // Handle logout or redirect to login page if refresh fails
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/login'; // Redirect to login page (or show a message)
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
