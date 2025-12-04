from django.contrib import admin
from .models import UserProfile, Event, RSVP, Review


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'location', 'created_at']
    search_fields = ['user__username', 'full_name', 'location']
    list_filter = ['created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'location', 'start_time', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    list_filter = ['is_public', 'start_time', 'created_at']
    filter_horizontal = ['invited_users']


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'created_at']
    search_fields = ['event__title', 'user__username']
    list_filter = ['status', 'created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'rating', 'created_at']
    search_fields = ['event__title', 'user__username', 'comment']
    list_filter = ['rating', 'created_at']
