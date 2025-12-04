from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Event, RSVP, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'full_name', 'bio', 
                  'location', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm Password')
    full_name = serializers.CharField(required=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'full_name', 'bio', 'location']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 and profile fields
        validated_data.pop('password2')
        full_name = validated_data.pop('full_name')
        bio = validated_data.pop('bio', '')
        location = validated_data.pop('location', '')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            bio=bio,
            location=location
        )
        
        return user


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model"""
    organizer = UserSerializer(read_only=True)
    organizer_id = serializers.IntegerField(write_only=True, required=False)
    rsvp_count = serializers.SerializerMethodField()
    user_rsvp_status = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    invited_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'organizer', 'organizer_id', 'location', 
                  'start_time', 'end_time', 'is_public', 'created_at', 'updated_at',
                  'rsvp_count', 'user_rsvp_status', 'average_rating', 'invited_users']
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer']

    def get_rsvp_count(self, obj):
        return obj.rsvps.filter(status='going').count()

    def get_user_rsvp_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rsvp = obj.rsvps.filter(user=request.user).first()
            return rsvp.status if rsvp else None
        return None

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None

    def validate(self, attrs):
        if attrs.get('end_time') and attrs.get('start_time'):
            if attrs['end_time'] <= attrs['start_time']:
                raise serializers.ValidationError({"end_time": "End time must be after start time."})
        return attrs


class RSVPSerializer(serializers.ModelSerializer):
    """Serializer for RSVP model"""
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'event', 'event_id', 'user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'event']

    def validate_status(self, value):
        if value not in ['going', 'maybe', 'not_going']:
            raise serializers.ValidationError("Invalid status. Choose from 'going', 'maybe', or 'not_going'.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'event_id', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'event']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
