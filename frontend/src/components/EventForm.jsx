import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { eventsAPI } from '../api/api';
import './Events.css';

const EventForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
    start_time: '',
    end_time: '',
    is_public: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isEdit) {
      fetchEvent();
    }
  }, [id]);

  const fetchEvent = async () => {
    try {
      const response = await eventsAPI.getById(id);
      const event = response.data;
      setFormData({
        title: event.title,
        description: event.description,
        location: event.location,
        start_time: event.start_time.slice(0, 16),
        end_time: event.end_time.slice(0, 16),
        is_public: event.is_public,
      });
    } catch (err) {
      setError('Failed to load event');
    }
  };

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = {
        ...formData,
        start_time: new Date(formData.start_time).toISOString(),
        end_time: new Date(formData.end_time).toISOString(),
      };

      if (isEdit) {
        await eventsAPI.update(id, data);
        alert('Event updated successfully!');
      } else {
        await eventsAPI.create(data);
        alert('Event created successfully!');
      }
      navigate('/events');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save event');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <div className="form-card">
        <h2>{isEdit ? 'Edit Event' : 'Create New Event'}</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Event Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="Enter event title"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="5"
              placeholder="Describe your event..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="location">Location *</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              placeholder="Event location"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_time">Start Time *</label>
              <input
                type="datetime-local"
                id="start_time"
                name="start_time"
                value={formData.start_time}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_time">End Time *</label>
              <input
                type="datetime-local"
                id="end_time"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="is_public"
                checked={formData.is_public}
                onChange={handleChange}
              />
              <span>Public Event (visible to everyone)</span>
            </label>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Saving...' : isEdit ? 'Update Event' : 'Create Event'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/events')}
              className="btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EventForm;
