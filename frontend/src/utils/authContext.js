import React, { createContext, useState, useEffect } from 'react';
import { login, refreshAccessToken } from './auth';
import {jwtDecode} from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const navigate = useNavigate(); // Ensure it's called unconditionally at the top level
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        console.log("Decoded Token:", decoded); // Log to check
        setUser(decoded);
      } catch (error) {
        console.error("Token decoding failed:", error);
      }
    }
  }, []);

  const handleLogin = async (email, password) => {
    try {
      const userData = await login(email, password);
      setUser(userData);
    } catch (error) {
      console.error('Login failed');
    }
  };

  const handleLogout = () => {
    // Clear authentication tokens and set the state to false
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null); // Reset user state

    // Navigate to login page and replace the current route to prevent the user from going back
    navigate('/login', { replace: true });
  };

  const refreshUserToken = async () => {
    try {
      const accessToken = await refreshAccessToken();
      const decoded = jwtDecode(accessToken);
      setUser(decoded);
    } catch (error) {
      console.error('Token refresh failed');
    }
  };

  const isAuthenticated = user !== null;

  return (
    <AuthContext.Provider value={{ user, handleLogin, handleLogout, isAuthenticated, refreshUserToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext, AuthProvider };
