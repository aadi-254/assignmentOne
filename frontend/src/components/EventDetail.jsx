import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { eventsAPI } from '../api/api';
import { useAuth } from '../context/AuthContext';
import './Events.css';

const EventDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  const [event, setEvent] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewForm, setReviewForm] = useState({ rating: 5, comment: '' });
  const [showReviewForm, setShowReviewForm] = useState(false);

  useEffect(() => {
    fetchEventDetails();
    fetchReviews();
  }, [id]);

  const fetchEventDetails = async () => {
    try {
      const response = await eventsAPI.getById(id);
      setEvent(response.data);
    } catch (err) {
      console.error('Failed to load event:', err);
      alert('Failed to load event details');
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await eventsAPI.getReviews(id);
      setReviews(response.data.results || []);
    } catch (err) {
      console.error('Failed to load reviews:', err);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      try {
        await eventsAPI.delete(id);
        alert('Event deleted successfully');
        navigate('/events');
      } catch (err) {
        alert('Failed to delete event');
      }
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    try {
      await eventsAPI.addReview(id, reviewForm);
      alert('Review submitted successfully!');
      setReviewForm({ rating: 5, comment: '' });
      setShowReviewForm(false);
      fetchReviews();
      fetchEventDetails(); // Refresh to update average rating
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to submit review');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return <div className="loading">Loading event...</div>;
  }

  if (!event) {
    return <div className="error-message">Event not found</div>;
  }

  const isOrganizer = user && event.organizer.id === user.id;

  return (
    <div className="event-detail-container">
      <div className="event-detail-header">
        <Link to="/events" className="back-link">
          ← Back to Events
        </Link>
        
        {isOrganizer && (
          <div className="organizer-actions">
            <Link to={`/events/${id}/edit`} className="btn-secondary">
              Edit Event
            </Link>
            <button onClick={handleDelete} className="btn-danger">
              Delete Event
            </button>
          </div>
        )}
      </div>

      <div className="event-detail-card">
        <div className="event-detail-badge">
          {event.is_public ? (
            <span className="badge-public">Public Event</span>
          ) : (
            <span className="badge-private">Private Event</span>
          )}
        </div>

        <h1>{event.title}</h1>
        
        <div className="event-meta">
          <div className="meta-item">
            <strong>Organized by:</strong> {event.organizer.username}
          </div>
          {event.average_rating && (
            <div className="meta-item">
              <strong>Rating:</strong> ⭐ {event.average_rating}/5
            </div>
          )}
          <div className="meta-item">
            <strong>RSVPs:</strong> {event.rsvp_count || 0} people going
          </div>
        </div>

        <div className="event-detail-section">
          <h3>Description</h3>
          <p>{event.description}</p>
        </div>

        <div className="event-detail-section">
          <h3>Event Details</h3>
          <div className="detail-grid">
            <div className="detail-item">
              <strong>📍 Location:</strong>
              <p>{event.location}</p>
            </div>
            <div className="detail-item">
              <strong>📅 Start Time:</strong>
              <p>{formatDate(event.start_time)}</p>
            </div>
            <div className="detail-item">
              <strong>⏰ End Time:</strong>
              <p>{formatDate(event.end_time)}</p>
            </div>
          </div>
        </div>

        {isAuthenticated && (
          <div className="event-detail-section">
            <h3>Your RSVP</h3>
            {event.user_rsvp_status && (
              <p>Current status: <strong>{event.user_rsvp_status}</strong></p>
            )}
            <div className="rsvp-buttons">
              <button
                onClick={() => eventsAPI.rsvp(id, 'going').then(fetchEventDetails)}
                className="btn-rsvp btn-going"
              >
                Going
              </button>
              <button
                onClick={() => eventsAPI.rsvp(id, 'maybe').then(fetchEventDetails)}
                className="btn-rsvp btn-maybe"
              >
                Maybe
              </button>
              <button
                onClick={() => eventsAPI.rsvp(id, 'not_going').then(fetchEventDetails)}
                className="btn-rsvp btn-not-going"
              >
                Not Going
              </button>
            </div>
          </div>
        )}

        <div className="event-detail-section">
          <h3>Reviews ({reviews.length})</h3>
          
          {isAuthenticated && !showReviewForm && (
            <button
              onClick={() => setShowReviewForm(true)}
              className="btn-secondary"
            >
              Write a Review
            </button>
          )}

          {showReviewForm && (
            <form onSubmit={handleReviewSubmit} className="review-form">
              <div className="form-group">
                <label>Rating (1-5)</label>
                <select
                  value={reviewForm.rating}
                  onChange={(e) =>
                    setReviewForm({ ...reviewForm, rating: parseInt(e.target.value) })
                  }
                  required
                >
                  <option value="5">5 - Excellent</option>
                  <option value="4">4 - Good</option>
                  <option value="3">3 - Average</option>
                  <option value="2">2 - Poor</option>
                  <option value="1">1 - Terrible</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>Comment</label>
                <textarea
                  value={reviewForm.comment}
                  onChange={(e) =>
                    setReviewForm({ ...reviewForm, comment: e.target.value })
                  }
                  rows="4"
                  required
                  placeholder="Share your thoughts about this event..."
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  Submit Review
                </button>
                <button
                  type="button"
                  onClick={() => setShowReviewForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="reviews-list">
            {reviews.length === 0 ? (
              <p>No reviews yet. Be the first to review!</p>
            ) : (
              reviews.map((review) => (
                <div key={review.id} className="review-card">
                  <div className="review-header">
                    <strong>{review.user.username}</strong>
                    <span className="review-rating">
                      {'⭐'.repeat(review.rating)}
                    </span>
                  </div>
                  <p className="review-comment">{review.comment}</p>
                  <p className="review-date">
                    {new Date(review.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetail;
