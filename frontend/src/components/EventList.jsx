import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { eventsAPI } from '../api/api';
import { useAuth } from '../context/AuthContext';
import './Events.css';

const EventList = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPublic, setFilterPublic] = useState('all');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const { isAuthenticated } = useAuth();

  useEffect(() => {
    fetchEvents();
  }, [page, searchTerm, filterPublic]);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        search: searchTerm,
      };
      
      if (filterPublic !== 'all') {
        params.is_public = filterPublic === 'public';
      }

      const response = await eventsAPI.getAll(params);
      setEvents(response.data.results);
      setTotalPages(Math.ceil(response.data.count / 10));
      setError('');
    } catch (err) {
      setError('Failed to load events');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRSVP = async (eventId, status) => {
    try {
      await eventsAPI.rsvp(eventId, status);
      fetchEvents(); // Refresh to show updated RSVP status
    } catch (err) {
      alert('Failed to RSVP. Please try again.');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div className="loading">Loading events...</div>;
  }

  return (
    <div className="events-container">
      <div className="events-header">
        <h1>Events</h1>
        {isAuthenticated && (
          <Link to="/events/create" className="btn-primary">
            Create Event
          </Link>
        )}
      </div>

      <div className="events-filters">
        <input
          type="text"
          placeholder="Search events..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        
        <select
          value={filterPublic}
          onChange={(e) => setFilterPublic(e.target.value)}
          className="filter-select"
        >
          <option value="all">All Events</option>
          <option value="public">Public Only</option>
          <option value="private">Private Only</option>
        </select>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="events-grid">
        {events.length === 0 ? (
          <p className="no-events">No events found</p>
        ) : (
          events.map((event) => (
            <div key={event.id} className="event-card">
              <div className="event-badge">
                {event.is_public ? (
                  <span className="badge-public">Public</span>
                ) : (
                  <span className="badge-private">Private</span>
                )}
              </div>

              <h3>{event.title}</h3>
              <p className="event-description">{event.description}</p>

              <div className="event-details">
                <div className="detail-item">
                  <strong>📍 Location:</strong> {event.location}
                </div>
                <div className="detail-item">
                  <strong>📅 Start:</strong> {formatDate(event.start_time)}
                </div>
                <div className="detail-item">
                  <strong>⏰ End:</strong> {formatDate(event.end_time)}
                </div>
                <div className="detail-item">
                  <strong>👤 Organizer:</strong> {event.organizer.username}
                </div>
                <div className="detail-item">
                  <strong>✅ RSVPs:</strong> {event.rsvp_count || 0} going
                </div>
                {event.average_rating && (
                  <div className="detail-item">
                    <strong>⭐ Rating:</strong> {event.average_rating}/5
                  </div>
                )}
              </div>

              {isAuthenticated && (
                <div className="event-actions">
                  {event.user_rsvp_status && (
                    <span className="rsvp-status">
                      Your RSVP: <strong>{event.user_rsvp_status}</strong>
                    </span>
                  )}
                  
                  <div className="rsvp-buttons">
                    <button
                      onClick={() => handleRSVP(event.id, 'going')}
                      className="btn-rsvp btn-going"
                    >
                      Going
                    </button>
                    <button
                      onClick={() => handleRSVP(event.id, 'maybe')}
                      className="btn-rsvp btn-maybe"
                    >
                      Maybe
                    </button>
                    <button
                      onClick={() => handleRSVP(event.id, 'not_going')}
                      className="btn-rsvp btn-not-going"
                    >
                      Not Going
                    </button>
                  </div>

                  <Link to={`/events/${event.id}`} className="btn-secondary">
                    View Details
                  </Link>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
            className="btn-pagination"
          >
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === totalPages}
            className="btn-pagination"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default EventList;
