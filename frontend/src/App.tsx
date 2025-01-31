import './App.css'
import TestAppPage from '@/pages/TestAppPage/TestAppPage'
import { HashRouter, Routes, Route } from 'react-router-dom';

export default function App() {
  return (
    <>
      <HashRouter>
        <Routes>
          <Route path="/test_app" element={<TestAppPage />} />
          <Route path="/" element={<div>Main Page</div>} />
          <Route path="*" element={<div>Not Found</div>} />
        </Routes>
      </HashRouter>
    </>
  )
}