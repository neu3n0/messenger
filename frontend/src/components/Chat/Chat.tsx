import React, { useEffect, useRef } from 'react';
import {
  useNavigate,
  useParams,
  useLocation
} from 'react-router-dom';
import styles from './Chat.module.scss'

import useIsMobile from '@/hooks/useIsMobile';

const ChatContent: React.FC<{ user_id: string }> = ({ user_id }) => {
  const messages = Array.from({ length: Number(user_id) * 10 || 0 }, (_, i) =>
    `Message ${i + 1} for contact ${user_id}`
  );

  const endRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'auto' });
  }, [user_id]);

  return (
    <div className={styles.chatContent}>
      {messages.map((msg, index) => (
        <div key={index} className={styles.message}>
          {msg}
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
};

export const ChatPlaceholder: React.FC = () => (
  <div className={styles.chatPlaceholder}>
    <p>Please select a contact to start chatting.</p>
  </div>
);

const ChatHeader: React.FC<{ openProfile: any, closeChat: any, mobile?: boolean, username: string }> = ({ openProfile, closeChat, mobile, username }) => {
  return (
    <header className={styles.chatHeader}>
      {mobile && (<button className={styles.back} onClick={closeChat}>Back</button>)}
      <h2 onClick={openProfile}>Chat with Contact {username}</h2>
    </header>
  )
}

const ChatInput: React.FC = () => {
  return (
    <div className={styles.chatInput}>
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
    <div className={`${styles.chat} ${hideSidebar ? ' hidden' : ''}`}>
      <ChatHeader openProfile={openProfile} closeChat={closeChat} username={user_id} />
      <ChatContent user_id={user_id} />
      <ChatInput />
    </div>
  );
};

export default Chat;