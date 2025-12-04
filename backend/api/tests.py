from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile, Event, RSVP, Review


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_user_profile(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            full_name='Test User',
            bio='Test bio',
            location='Test City'
        )
        self.assertEqual(profile.full_name, 'Test User')
        self.assertEqual(str(profile), 'Test User (testuser)')


class EventModelTest(TestCase):
    """Test cases for Event model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='testpass123'
        )

    def test_create_event(self):
        """Test creating an event"""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.user,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.organizer, self.user)
        self.assertTrue(event.is_public)


class RSVPModelTest(TestCase):
    """Test cases for RSVP model"""

    def setUp(self):
        self.organizer = User.objects.create_user(
            username='organizer',
            password='testpass123'
        )
        self.attendee = User.objects.create_user(
            username='attendee',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.organizer,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )

    def test_create_rsvp(self):
        """Test creating an RSVP"""
        rsvp = RSVP.objects.create(
            event=self.event,
            user=self.attendee,
            status='going'
        )
        self.assertEqual(rsvp.status, 'going')
        self.assertEqual(rsvp.event, self.event)
        self.assertEqual(rsvp.user, self.attendee)


class ReviewModelTest(TestCase):
    """Test cases for Review model"""

    def setUp(self):
        self.organizer = User.objects.create_user(
            username='organizer',
            password='testpass123'
        )
        self.reviewer = User.objects.create_user(
            username='reviewer',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.organizer,
            location='Test Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )

    def test_create_review(self):
        """Test creating a review"""
        review = Review.objects.create(
            event=self.event,
            user=self.reviewer,
            rating=5,
            comment='Great event!'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great event!')


class EventAPITest(APITestCase):
    """Test cases for Event API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_event(self):
        """Test creating an event via API"""
        data = {
            'title': 'API Test Event',
            'description': 'API Test Description',
            'location': 'API Test Location',
            'start_time': (timezone.now() + timedelta(days=1)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
            'is_public': True
        }
        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Event')

    def test_list_events(self):
        """Test listing events via API"""
        Event.objects.create(
            title='Public Event',
            description='Description',
            organizer=self.user,
            location='Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_update_event_as_organizer(self):
        """Test updating event as organizer"""
        event = Event.objects.create(
            title='Original Title',
            description='Description',
            organizer=self.user,
            location='Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/events/{event.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_event_as_organizer(self):
        """Test deleting event as organizer"""
        event = Event.objects.create(
            title='Event to Delete',
            description='Description',
            organizer=self.user,
            location='Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        response = self.client.delete(f'/api/events/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RSVPAPITest(APITestCase):
    """Test cases for RSVP API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.organizer = User.objects.create_user(
            username='organizer',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Description',
            organizer=self.organizer,
            location='Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        self.client.force_authenticate(user=self.user)

    def test_rsvp_to_event(self):
        """Test RSVPing to an event"""
        data = {'status': 'going'}
        response = self.client.post(f'/api/events/{self.event.id}/rsvp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'going')

    def test_update_rsvp_status(self):
        """Test updating RSVP status"""
        RSVP.objects.create(event=self.event, user=self.user, status='going')
        data = {'status': 'maybe'}
        response = self.client.post(f'/api/events/{self.event.id}/rsvp/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'maybe')


class ReviewAPITest(APITestCase):
    """Test cases for Review API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.organizer = User.objects.create_user(
            username='organizer',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            description='Description',
            organizer=self.organizer,
            location='Location',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            is_public=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_review(self):
        """Test creating a review"""
        data = {
            'rating': 5,
            'comment': 'Great event!'
        }
        response = self.client.post(f'/api/events/{self.event.id}/review/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)

    def test_list_reviews_for_event(self):
        """Test listing reviews for an event"""
        Review.objects.create(
            event=self.event,
            user=self.user,
            rating=4,
            comment='Good event'
        )
        response = self.client.get(f'/api/events/{self.event.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class AuthenticationAPITest(APITestCase):
    """Test cases for Authentication endpoints"""

    def test_register_user(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'full_name': 'New User'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'newuser')

    def test_login_user(self):
        """Test user login with JWT"""
        user = User.objects.create_user(
            username='loginuser',
            password='loginpass123'
        )
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
