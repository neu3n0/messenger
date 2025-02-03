import React, { useState, useEffect } from "react"

import { TestAppType, UpdateTestAppType } from "@/types/testAppTypes";
import { getListTestApp, updateTestApp } from "@/api/testAppApi";

const TestAppPage: React.FC = () => {
  const [data, setData] = useState<TestAppType[] | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [testVal, setTestVal] = useState<number>(1);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getListTestApp();
        setData(response.data);
        console.log(response.data)
      } catch (error) {
        setError('Upload error');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 2000);
    return () => clearInterval(intervalId);

  }, [loading]);

  const handleUpdate = async () => {
    setError(null);
    const payload: UpdateTestAppType = {
      arg2: testVal,
    };

    try {
      await updateTestApp(1, payload);
    } catch (error) {
      setError('Update TestApp error');
      console.error(error);
    }
    if (testVal == 1) setTestVal(3);
    if (testVal == 3) setTestVal(1);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <>
      <div>
        {data && data.map(item => (
          <div key={item.id}>id = {item.id}: {item.arg1}, {item.arg2}</div>
        ))}
      </div>
      <button onClick={handleUpdate}>
        Update arg2 with id 1
      </button>
    </>
  )
}

export default TestAppPage;