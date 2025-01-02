import React from "react";
import { Navigate } from "react-router-dom";

// Helper function to decode JWT and extract the user's role
const getRoleFromToken = (token) => {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => `%${("00" + c.charCodeAt(0).toString(16)).slice(-2)}`)
        .join("")
    );
    const decodedToken = JSON.parse(jsonPayload);
    return decodedToken.role; // Assuming the JWT has a "role" field
  } catch (error) {
    console.error("Invalid token", error);
    return null;
  }
};

const PrivateRoute = ({ children, role }) => {
  const token = localStorage.getItem("access");
  const userRole = token ? getRoleFromToken(token) : null;

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (role && userRole !== role) {
    return <Navigate to="/" />;
  }

  return children;
};

export default PrivateRoute;
