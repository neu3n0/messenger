import './App.css';

import { useState, useEffect } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';


import TestAppPage from '@/pages/TestAppPage/TestAppPage';
import MainPage from '@/pages/MainPage/MainPage';
import LoginPage from '@/pages/LoginPage/LoginPage';
import PrivateRoute from '@/components/PrivateRoute/PrivateRoute';
import { retrieveProfile } from '@/api/userApi';
import { useAuthStore } from '@/stores/authStore';

export default function App() {
  const { setAuth, logout } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // When the application is loaded, we check if the session is valid,
    // by calling a secure endpoint (e.g. /api/profile/).
    // It is assumed that if the tokens in httpOnly cookies are valid,
    // the server will return the profile data.
    async function checkAuth() {
      try {
        const profile = await retrieveProfile();
        // If the request is successful, update Zustand: the user is authorised.
        setAuth(true, profile.username);
        console.log("username: ", profile.username);
      } catch (error) {
        // If 401 clear (logout) state
        logout();
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, [setAuth, logout]);


  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <HashRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/test_app" element={<TestAppPage />} />
          <Route element={<PrivateRoute />}>
            <Route path="/*" element={<MainPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </HashRouter>
    </div>
  );
}