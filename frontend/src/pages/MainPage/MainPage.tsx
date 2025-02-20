import LeftSidebar from '@/components/LeftSidebar/LeftSidebar';
import Chat, { ChatPlaceholder } from '@/components/Chat/Chat';
import RightSidebar from '@/components/RightSidebar/RightSidebar';
import React from 'react';
import { Routes, Route } from 'react-router-dom';

const MainPage: React.FC = () => {
  return (
    <>
      <LeftSidebar />
      <Routes>
        <Route path="/:user_id/*" element={<Chat />} />
        <Route path="*" element={<ChatPlaceholder />} />
      </Routes>
      {/* If URL contains /profile it will appear */}
      <Routes>
        <Route path="/:user_id/profile" element={<RightSidebar />} />
      </Routes>
    </>
  );
};

export default MainPage;