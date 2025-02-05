import React from 'react';
import styles from './RightSidebar.module.scss'

import { useNavigate, useParams } from 'react-router-dom';

const RightSidebar: React.FC = () => {
  const { user_id } = useParams();

  const navigate = useNavigate();
  const closeRightSidebar = () => { navigate(`/${user_id}`); };

  return (
    <div className={styles.rightSidebar}>
      <button className="back" onClick={closeRightSidebar}>
        X
      </button>
      <h2>Profile of Contact {user_id}</h2>
      <p>Here is the profile information...</p>
    </div>
  );
};

export default RightSidebar;