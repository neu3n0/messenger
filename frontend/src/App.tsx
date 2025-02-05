import './App.css';

import {
  HashRouter,
  Routes,
  Route,
} from 'react-router-dom';

import TestAppPage from '@/pages/TestAppPage/TestAppPage';
import MainPage from '@/pages/MainPage/MainPage';

export default function App() {
  return (
    <div className="App">
      <HashRouter>
        <Routes>
          <Route path="/test_app" element={<TestAppPage />} />
          <Route path="*" element={<MainPage />} />
        </Routes>
      </HashRouter>
    </div>
  );
}