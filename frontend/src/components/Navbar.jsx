import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🎉 Event Manager
        </Link>

        <div className="navbar-menu">
          <Link to="/events" className="navbar-link">
            Events
          </Link>

          {isAuthenticated ? (
            <>
              <Link to="/events/create" className="navbar-link">
                Create Event
              </Link>
              <span className="navbar-user">
                Hello, {user?.username}!
              </span>
              <button onClick={logout} className="navbar-button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Login
              </Link>
              <Link to="/register" className="navbar-button">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
