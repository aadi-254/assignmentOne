import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  getCurrentUser: () => api.get('/auth/me/'),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

// Events API
export const eventsAPI = {
  getAll: (params) => api.get('/events/', { params }),
  getById: (id) => api.get(`/events/${id}/`),
  create: (data) => api.post('/events/', data),
  update: (id, data) => api.patch(`/events/${id}/`, data),
  delete: (id) => api.delete(`/events/${id}/`),
  rsvp: (id, status) => api.post(`/events/${id}/rsvp/`, { status }),
  getRSVPs: (id) => api.get(`/events/${id}/rsvps/`),
  addReview: (id, data) => api.post(`/events/${id}/review/`, data),
  getReviews: (id, params) => api.get(`/events/${id}/reviews/`, { params }),
};

// Reviews API
export const reviewsAPI = {
  getAll: (params) => api.get('/reviews/', { params }),
  getById: (id) => api.get(`/reviews/${id}/`),
  update: (id, data) => api.patch(`/reviews/${id}/`, data),
  delete: (id) => api.delete(`/reviews/${id}/`),
};

// RSVPs API
export const rsvpsAPI = {
  getAll: () => api.get('/rsvps/'),
  getById: (id) => api.get(`/rsvps/${id}/`),
  update: (id, data) => api.patch(`/rsvps/${id}/`, data),
  delete: (id) => api.delete(`/rsvps/${id}/`),
};

// Profiles API
export const profilesAPI = {
  getAll: () => api.get('/profiles/'),
  getById: (id) => api.get(`/profiles/${id}/`),
  update: (id, data) => api.patch(`/profiles/${id}/`, data),
};

export default api;
