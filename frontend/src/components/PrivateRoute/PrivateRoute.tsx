import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

const PrivateRoute: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  console.log("isAuthenticated: ", isAuthenticated);
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;