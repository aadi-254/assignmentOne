# 🎉 Event Management System

A full-stack Event Management System built with **Django REST Framework** (backend) and **React** (frontend). This application allows users to create, manage, and RSVP to events with authentication, custom permissions, and real-time updates.

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![React](https://img.shields.io/badge/React-19.2.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Backend (Django REST Framework)
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **User Profiles** - Extended user model with profile information
- ✅ **Event Management** - CRUD operations for events
- ✅ **RSVP System** - Users can RSVP with status (Going/Maybe/Not Going)
- ✅ **Review System** - Rate and review events
- ✅ **Custom Permissions** - Organizer-only edits, private event access
- ✅ **Pagination & Filtering** - Efficient data retrieval
- ✅ **Search Functionality** - Search events by title, description, location
- ✅ **MySQL Support** - Production-ready database configuration
- ✅ **Admin Panel** - Django admin for easy management
- ✅ **Unit Tests** - 35+ comprehensive tests

### Frontend (React)
- ✅ **Modern UI** - Responsive design with custom CSS
- ✅ **Authentication Flow** - Login, Register, Logout
- ✅ **Event Listing** - Browse all public events
- ✅ **Event Details** - View event information and reviews
- ✅ **Event Creation/Editing** - Create and manage your events
- ✅ **RSVP Management** - Quick RSVP to events
- ✅ **Review Submission** - Rate and review events you've attended
- ✅ **Protected Routes** - Secure routes for authenticated users
- ✅ **Token Refresh** - Automatic JWT token refresh

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.6** - High-level Python web framework
- **Django REST Framework 3.16.1** - Powerful API toolkit
- **djangorestframework-simplejwt 5.5.1** - JWT authentication
- **django-cors-headers 4.9.0** - CORS support
- **django-filter 25.2** - Advanced filtering
- **MySQL/SQLite** - Database options
- **Pillow 11.0.0** - Image processing

### Frontend
- **React 19.2.0** - UI library
- **Vite 7.2.4** - Fast build tool
- **React Router 7.10.1** - Client-side routing
- **Axios 1.13.2** - HTTP client
- **CSS3** - Custom styling

---

## 📁 Project Structure

```
Event-Management-System/
│
├── backend/                    # Django REST API
│   ├── api/                    # Main API application
│   │   ├── models.py          # Database models (User, Event, RSVP, Review)
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API views and ViewSets
│   │   ├── permissions.py     # Custom permission classes
│   │   ├── urls.py            # API URL routing
│   │   ├── admin.py           # Admin panel configuration
│   │   └── tests.py           # Unit tests
│   │
│   ├── backend/               # Project settings
│   │   ├── settings.py        # Django configuration
│   │   └── urls.py            # Main URL routing
│   │
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   └── database_schema.sql    # MySQL schema reference
│
└── frontend/                  # React Frontend
    ├── src/
    │   ├── api/               # API client
    │   │   └── api.js         # Axios instance with interceptors
    │   │
    │   ├── components/        # React components
    │   │   ├── Home.jsx       # Landing page
    │   │   ├── Login.jsx      # Login component
    │   │   ├── Register.jsx   # Registration component
    │   │   ├── EventList.jsx  # Event listing with filters
    │   │   ├── EventDetail.jsx # Event details with reviews
    │   │   ├── EventForm.jsx  # Create/Edit event form
    │   │   └── Navbar.jsx     # Navigation bar
    │   │
    │   ├── context/           # React context
    │   │   └── AuthContext.jsx # Authentication state
    │   │
    │   ├── App.jsx            # Main app component
    │   └── main.jsx           # Entry point
    │
    ├── package.json           # npm dependencies
    └── vite.config.js         # Vite configuration
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- MySQL (optional, can use SQLite)
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/aadi-254/assignmentOne.git
cd assignmentOne
```

2. **Create virtual environment**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**

For **SQLite** (Development - Default):
```python
# backend/settings.py is already configured for SQLite
```

For **MySQL** (Production):
```python
# In backend/settings.py, uncomment MySQL config and update:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'event_management_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Backend will be available at: **http://localhost:8000/**

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

Frontend will be available at: **http://localhost:5173/**

---

## 🎯 Usage

### Accessing the Application

1. **Frontend**: Open http://localhost:5173/
2. **Backend API**: http://localhost:8000/api/
3. **Admin Panel**: http://localhost:8000/admin/

### User Flow

1. **Register** - Create a new account with profile information
2. **Login** - Authenticate with username and password
3. **Browse Events** - View all public events on the home page
4. **Create Event** - Click "Create Event" to add a new event
5. **RSVP** - Respond to events (Going/Maybe/Not Going)
6. **Review** - Rate and review events after attending
7. **Manage Events** - Edit or delete your own events

### Admin Features

Access the admin panel at http://localhost:8000/admin/ to:
- Manage all users and profiles
- View and moderate all events
- Review RSVPs and reviews
- Manage system data

---

## 📡 API Endpoints

### Authentication
```
POST   /api/auth/register/      - Register new user
POST   /api/auth/login/         - Login and get JWT tokens
POST   /api/auth/token/refresh/ - Refresh access token
GET    /api/auth/me/            - Get current user profile
```

### Events
```
GET    /api/events/             - List all events (with pagination)
POST   /api/events/             - Create new event
GET    /api/events/{id}/        - Get event details
PUT    /api/events/{id}/        - Update event (organizer only)
DELETE /api/events/{id}/        - Delete event (organizer only)
POST   /api/events/{id}/rsvp/   - RSVP to event
GET    /api/events/{id}/rsvps/  - Get event RSVPs
POST   /api/events/{id}/review/ - Submit review
GET    /api/events/{id}/reviews/ - Get event reviews
```

### Query Parameters
```
?page=1                  - Pagination
?search=keyword          - Search events
?is_public=true          - Filter by public/private
?location=City           - Filter by location
?ordering=-start_time    - Sort results
```

### User Profiles
```
GET    /api/profiles/           - List user profiles
GET    /api/profiles/{id}/      - Get profile details
PUT    /api/profiles/{id}/      - Update profile
```

### RSVPs
```
GET    /api/rsvps/              - List user's RSVPs
POST   /api/rsvps/              - Create RSVP
PUT    /api/rsvps/{id}/         - Update RSVP
DELETE /api/rsvps/{id}/         - Delete RSVP
```

### Reviews
```
GET    /api/reviews/            - List user's reviews
POST   /api/reviews/            - Create review
PUT    /api/reviews/{id}/       - Update review
DELETE /api/reviews/{id}/       - Delete review
```

---

## 🧪 Testing

Run backend tests:
```bash
cd backend
python manage.py test
```

The project includes 35+ unit tests covering:
- Model creation and validation
- API endpoints and authentication
- Custom permissions
- RSVP and review functionality

---

## 🔐 Security Features

- ✅ JWT token authentication
- ✅ Password hashing
- ✅ CORS protection
- ✅ Custom permission classes
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ CSRF protection

---

## 🌟 Key Features Explained

### 1. Authentication System
- JWT-based authentication with access and refresh tokens
- Automatic token refresh on expiration
- Protected routes in frontend
- Secure password storage

### 2. Permission System
- **IsOrganizerOrReadOnly**: Only event organizers can edit/delete
- **IsInvitedToPrivateEvent**: Private events visible only to invited users
- **IsOwnerOrReadOnly**: Users can only edit their own RSVPs/reviews

### 3. Event Privacy
- **Public Events**: Visible to all users
- **Private Events**: Only visible to organizer and invited users
- Event organizers can invite specific users

### 4. RSVP System
- Three status options: Going, Maybe, Not Going
- One RSVP per user per event
- Real-time RSVP counts on events

### 5. Review System
- Rating system (1-5 stars)
- Text reviews
- Average rating calculation
- One review per user per event

---

## 📸 Screenshots

### Home Page
Browse all public events with search and filter options.

### Event Details
View full event information, RSVPs, and reviews.

### Create Event
Easy-to-use form for creating new events.

### Admin Panel
Manage all system data through Django admin.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Aditya Makwana**
- GitHub: [@aadi-254](https://github.com/aadi-254)
- Email: adityamakwana254@gmail.com

---

## 🙏 Acknowledgments

- Django REST Framework documentation
- React documentation
- Material Design guidelines
- Stack Overflow community

---

## 📞 Support

For support, email adityamakwana254@gmail.com or open an issue on GitHub.

---

## 🔮 Future Enhancements

- [ ] Email notifications for event reminders
- [ ] Calendar integration
- [ ] Event categories and tags
- [ ] Social media sharing
- [ ] Event analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Real-time chat for events
- [ ] Payment integration for paid events
- [ ] Geolocation-based event discovery
- [ ] Event recommendations

---

**⭐ If you like this project, please give it a star on GitHub! ⭐**
