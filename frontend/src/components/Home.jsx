import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1 className="hero-title">Welcome to Event Manager</h1>
        <p className="hero-subtitle">
          Organize, discover, and join amazing events in your community
        </p>
        <div className="hero-buttons">
          <Link to="/events" className="btn-hero-primary">
            Browse Events
          </Link>
          <Link to="/register" className="btn-hero-secondary">
            Get Started
          </Link>
        </div>
      </div>

      <div className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎫</div>
            <h3>Create Events</h3>
            <p>Easily create and manage your own events with our intuitive interface</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">👥</div>
            <h3>RSVP System</h3>
            <p>Let attendees RSVP to your events and track attendance effortlessly</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">⭐</div>
            <h3>Reviews & Ratings</h3>
            <p>Share feedback and rate events to help others make informed decisions</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Privacy Controls</h3>
            <p>Create public or private events with invite-only access</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Search & Filter</h3>
            <p>Find events by location, date, or category with powerful search tools</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">📱</div>
            <h3>Real-time Updates</h3>
            <p>Stay informed with instant notifications about event changes</p>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <h2>Ready to get started?</h2>
        <p>Join thousands of event organizers and attendees today!</p>
        <Link to="/register" className="btn-cta">
          Create Your Account
        </Link>
      </div>
    </div>
  );
};

export default Home;
