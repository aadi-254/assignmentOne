from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from .models import UserProfile, Event, RSVP, Review
from .serializers import (
    UserSerializer, UserProfileSerializer, RegisterSerializer,
    EventSerializer, RSVPSerializer, ReviewSerializer
)
from .permissions import IsOrganizerOrReadOnly, IsInvitedToPrivateEvent, IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile CRUD operations"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only view their own profile
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event CRUD operations"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly, IsInvitedToPrivateEvent]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'is_public', 'organizer']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_time', 'created_at', 'title']

    def get_queryset(self):
        """
        Filter queryset to show:
        - All public events
        - Private events where user is organizer or invited
        """
        user = self.request.user
        
        # If user is staff, show all events
        if user.is_authenticated and user.is_staff:
            return Event.objects.all()
        
        # If user is not authenticated, show only public events
        if not user.is_authenticated:
            return Event.objects.filter(is_public=True)
        
        # If user is authenticated, show public events + their private events
        from django.db.models import Q
        return Event.objects.filter(
            Q(is_public=True) | 
            Q(organizer=user) | 
            Q(invited_users=user)
        ).distinct()

    def perform_create(self, serializer):
        """Set the organizer to the current user when creating an event"""
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rsvp(self, request, pk=None):
        """RSVP to an event"""
        event = self.get_object()
        status_value = request.data.get('status', 'going')

        if status_value not in ['going', 'maybe', 'not_going']:
            return Response(
                {'error': 'Invalid status. Choose from: going, maybe, not_going'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rsvp, created = RSVP.objects.update_or_create(
            event=event,
            user=request.user,
            defaults={'status': status_value}
        )

        serializer = RSVPSerializer(rsvp, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rsvps(self, request, pk=None):
        """Get all RSVPs for an event"""
        event = self.get_object()
        rsvps = event.rsvps.all()
        serializer = RSVPSerializer(rsvps, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        """Add a review for an event"""
        event = self.get_object()
        
        # Check if user already reviewed
        if Review.objects.filter(event=event, user=request.user).exists():
            return Response(
                {'error': 'You have already reviewed this event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for an event"""
        event = self.get_object()
        reviews = event.reviews.all()
        
        # Pagination
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(reviews, request)
        
        serializer = ReviewSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class RSVPViewSet(viewsets.ModelViewSet):
    """ViewSet for RSVP CRUD operations"""
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Users can only view their own RSVPs"""
        if self.request.user.is_staff:
            return RSVP.objects.all()
        return RSVP.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating an RSVP"""
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review CRUD operations"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Filter reviews by event if event_id is provided"""
        queryset = Review.objects.all()
        event_id = self.request.query_params.get('event_id')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review"""
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user"""
    serializer = UserSerializer(request.user)
    profile = UserProfile.objects.filter(user=request.user).first()
    profile_data = UserProfileSerializer(profile).data if profile else None
    
    return Response({
        'user': serializer.data,
        'profile': profile_data
    })
