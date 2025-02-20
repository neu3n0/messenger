import React, { useState } from 'react';
import styles from './LeftSidebar.module.scss'

import useIsMobile from '@/hooks/useIsMobile';
import ThemeToggle from '@/components/common/ThemeToggle/ThemeToggle';

import { Link, useLocation } from 'react-router-dom';

const LeftSidebar: React.FC = () => {
  const location = useLocation();
  const isMobile = useIsMobile();
  const hideSidebar = isMobile && location.pathname !== '/';
  const [page, setPage] = useState<"settings" | "contacts">("contacts");

  return (
    <aside className={`${styles.leftSidebar}${hideSidebar ? ' hidden' : ''}`}>
      <div className={`${page !== "contacts" ? ' hidden' : ''}`}>
        <div className="search">
          <input type="text" placeholder="Search..." />
        </div>
        <ul className="contacts">
          <li> <Link to="/2">Contact 2</Link> </li>
          <li> <Link to="/4">Contact 4</Link> </li>
          <li> <Link to="/6">Contact 6</Link> </li>
        </ul>
        <ThemeToggle />
        <button onClick={() => setPage("settings")}>---</button>
      </div>
      {
        page == "settings" &&
        <div>
          <span>Settings</span>
          <button onClick={() => setPage("contacts")}>---</button>
        </div>
      }
    </aside>
  );
};

export default LeftSidebar;