import './App.css';

import React, { useEffect, useRef } from 'react';
import {
  HashRouter,
  Routes,
  Route,
  useNavigate,
  useParams,
  Link,
  useLocation
} from 'react-router-dom';

import useIsMobile from '@/hooks/useIsMobile';
import ThemeToggle from '@/components/common/ThemeToggle/ThemeToggle';
import TestAppPage from '@/pages/TestAppPage/TestAppPage';

const LeftSidebar: React.FC = () => {
  const location = useLocation();
  const isMobile = useIsMobile();
  const hideSidebar = isMobile && location.pathname !== '/';
  // if (hideSidebar) return <></>

  return (
    <aside className={`left-sidebar${hideSidebar ? ' hidden' : ''}`}>
      <div className="search">
        <input type="text" placeholder="Search..." />
      </div>
      <ul className="contacts">
        <li> <Link to="/2">Contact 2</Link> </li>
        <li> <Link to="/4">Contact 4</Link> </li>
        <li> <Link to="/6">Contact 6</Link> </li>
      </ul>
      <ThemeToggle />
    </aside>
  );
};

const RightSidebar: React.FC = () => {
  const { user_id } = useParams();

  const navigate = useNavigate();
  const closeRightSidebar = () => { navigate(`/${user_id}`); };

  return (
    <div className="right-sidebar">
      <button className="back" onClick={closeRightSidebar}>
        X
      </button>
      <h2>Profile of Contact {user_id}</h2>
      <p>Here is the profile information...</p>
    </div>
  );
};

const ChatContent: React.FC<{ user_id: string }> = ({ user_id }) => {
  const messages = Array.from({ length: Number(user_id) * 10 || 0 }, (_, i) =>
    `Message ${i + 1} for contact ${user_id}`
  );

  const endRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'auto' });
  }, [user_id]);

  return (
    <div className="chat-content">
      {messages.map((msg, index) => (
        <div key={index} className="message">
          {msg}
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
};

const ChatPlaceholder: React.FC = () => (
  <div className="chat-placeholder">
    <p>Please select a contact to start chatting.</p>
  </div>
);

const ChatHeader: React.FC<{ openProfile: any, closeChat: any, mobile?: boolean, username: string }> = ({ openProfile, closeChat, mobile, username }) => {
  return (
    <header className="chat-header">
      {mobile && (<button className="back" onClick={closeChat}>Back</button>)}
      <h2 onClick={openProfile}>Chat with Contact {username}</h2>
    </header>
  )
}

const ChatInput: React.FC = () => {
  return (
    <div className="chat-input">
      <input type="text" placeholder="Type a message..." />
      <button>Send</button>
    </div>
  )
}

const Chat: React.FC = () => {
  const { user_id } = useParams();
  if (!user_id) return <ChatPlaceholder />;

  const navigate = useNavigate();
  const openProfile = () => { navigate(`/${user_id}/profile`); };
  const closeChat = () => { navigate('/'); };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { navigate('/'); }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [navigate]);

  const location = useLocation();
  const isMobile = useIsMobile();
  const hideSidebar = isMobile && location.pathname !== `/${user_id}`;

  return (
    <div className={`chat ${hideSidebar ? ' hidden' : ''}`}>
      <ChatHeader openProfile={openProfile} closeChat={closeChat} username={user_id} />
      <ChatContent user_id={user_id} />
      <ChatInput />
    </div>
  );
};

const DesktopLayout: React.FC = () => {
  return (
    <>
      <LeftSidebar />
      <Routes>
        <Route path="/" element={<ChatPlaceholder />} />
        <Route path="/:user_id" element={<Chat />} />
        <Route path="*" element={<ChatPlaceholder />} />
      </Routes>
      {/* If URL contains /profile it will appear */}
      <Routes>
        <Route path="/:user_id/profile" element={<RightSidebar />} />
      </Routes>
    </>
  );
};

export default function App() {
  return (
    <div className="App">
      <HashRouter>
        <Routes>
          <Route path="/test_app" element={<TestAppPage />} />
          <Route path="*" element={<DesktopLayout />} />
        </Routes>
      </HashRouter>
    </div>
  );
}