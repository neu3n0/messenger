import React, { useEffect, useState } from "react"
import { useNavigate } from 'react-router-dom';

import { fetchTestApps, updateTestApp, createTestApp } from "@/api/testAppApi";
import { logoutUser } from "@/api/auth";

import { TestAppType } from "@/types/testAppTypes";

import { useAuthStore } from '@/stores/authStore';

const TestAppPage: React.FC = () => {
  const [testApps, setTestApps] = useState<TestAppType[]>([]);
  const [arg1, setArg1] = useState<string>('');
  const [arg2, setArg2] = useState<number>(0);
  const [selectedTest, setSelectedTest] = useState<TestAppType | null>(null);
  const { logout } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const loadTestApps = async () => {
      try {
        const data = await fetchTestApps();
        setTestApps(data);
      } catch (error) {
        console.error('Error fetching TestApps:', error);
      }
    };
    loadTestApps();
    const intervalId = setInterval(loadTestApps, 2000);
    return () => clearInterval(intervalId);
  }, [])

  const handleCreateTestApp = async () => {
    try {
      const newTest = await createTestApp({ arg1, arg2 });
      setTestApps([...testApps, newTest]);
      setArg1('');
      setArg2(0);
    } catch (error) {
      console.error('Error creating TestApp:', error);
    }
  };

  const handleUpdateTestApp = async () => {
    if (!selectedTest) return;
    try {
      const updatedTest = await updateTestApp(selectedTest.id, { arg1, arg2 });
      setTestApps(testApps.map((t) => (t.id === updatedTest.id ? updatedTest : t)));
      setSelectedTest(null);
      setArg1('');
      setArg2(0);
    } catch (error) {
      console.error('Error updating TestApp:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
      logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div>
      <h1>TestApp Demo</h1>
      <div>
        <input
          placeholder="arg1"
          value={arg1}
          onChange={(e) => setArg1(e.target.value)}
        />
        <input
          type="number"
          placeholder="arg2"
          value={arg2}
          onChange={(e) => setArg2(parseFloat(e.target.value))}
        />
        {selectedTest ? (
          <button onClick={handleUpdateTestApp}>Update TestApp</button>
        ) : (
          <button onClick={handleCreateTestApp}>Create TestApp</button>
        )}
      </div>
      <ul>
        {testApps.map((test) => (
          <li key={test.id}>
            <strong>{test.arg1}</strong> ({test.arg2}) by {test.owner}
            <button
              onClick={() => {
                setSelectedTest(test);
                setArg1(test.arg1);
                setArg2(test.arg2);
              }}
            >
              Edit
            </button>
          </li>
        ))}
      </ul>
      <button onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
};

export default TestAppPage;
