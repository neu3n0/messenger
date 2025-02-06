import React, { useState } from "react"

import { login } from "@/api/auth";
import { fetchTestApps, updateTestApp, createTestApp } from "@/api/testAppApi";
import { TestAppType } from "@/types/testAppTypes";

const TestAppPage: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  const [testApps, setTestApps] = useState<TestAppType[]>([]);
  const [arg1, setArg1] = useState<string>('');
  const [arg2, setArg2] = useState<number>(0);
  const [selectedTest, setSelectedTest] = useState<TestAppType | null>(null);

  // const [loading, setLoading] = useState<boolean>(true);
  // const [error, setError] = useState<string | null>(null);

  const loadTestApps = async () => {
    try {
      const data = await fetchTestApps();
      setTestApps(data);
    } catch (error) {
      console.error('Error fetching TestApps:', error);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login({ username: loginUsername, password: loginPassword });
      setIsLoggedIn(true);
      loadTestApps();
    } catch (error) {
      console.error('Login error:', error);
    }
  };

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

  return (
    <div>
      <h1>TestApp Demo</h1>
      {!isLoggedIn ? (
        <form onSubmit={handleLogin}>
          <h2>Login</h2>
          <div>
            <input
              type="text"
              placeholder="Username"
              value={loginUsername}
              onChange={(e) => setLoginUsername(e.target.value)}
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login</button>
        </form>
      ) : (
        <>
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
        </>
      )}
    </div>
  );
};

export default TestAppPage;



// import React, { useState, useEffect } from "react"

// import { TestAppType, UpdateTestAppType } from "@/types/testAppTypes";
// import { getListTestApp, updateTestApp } from "@/api/testAppApi";

// const TestAppPage: React.FC = () => {
//   const [data, setData] = useState<TestAppType[] | null>(null);
//   const [loading, setLoading] = useState<boolean>(true);
//   const [error, setError] = useState<string | null>(null);
//   const [testVal, setTestVal] = useState<number>(1);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await getListTestApp();
//         setData(response.data);
//         console.log(response.data)
//       } catch (error) {
//         setError('Upload error');
//         console.error(error);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchData();
//     const intervalId = setInterval(fetchData, 2000);
//     return () => clearInterval(intervalId);

//   }, [loading]);

//   const handleUpdate = async () => {
//     setError(null);
//     const payload: UpdateTestAppType = {
//       arg2: testVal,
//     };

//     try {
//       await updateTestApp(1, payload);
//     } catch (error) {
//       setError('Update TestApp error');
//       console.error(error);
//     }
//     if (testVal == 1) setTestVal(3);
//     if (testVal == 3) setTestVal(1);
//   };

//   if (loading) return <div>Loading...</div>;
//   if (error) return <div>{error}</div>;

//   return (
//     <>
//       <div>
//         {data && data.map(item => (
//           <div key={item.id}>id = {item.id}: {item.arg1}, {item.arg2}</div>
//         ))}
//       </div>
//       <button onClick={handleUpdate}>
//         Update arg2 with id 1
//       </button>
//     </>
//   )
// }

// export default TestAppPage;