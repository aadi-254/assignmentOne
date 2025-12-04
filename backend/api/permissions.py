from rest_framework import permissions


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an event to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the organizer
        return obj.organizer == request.user


class IsInvitedToPrivateEvent(permissions.BasePermission):
    """
    Custom permission to restrict access to private events to invited users only.
    """

    def has_permission(self, request, view):
        # Allow all users to list/retrieve events (queryset filtering handles private events)
        if view.action in ['list', 'retrieve']:
            return True
        
        # For create/update/delete actions, require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If event is public, allow access
        if obj.is_public:
            return True

        # If user is not authenticated, deny access to private events
        if not request.user.is_authenticated:
            return False

        # Allow access if user is the organizer
        if obj.organizer == request.user:
            return True

        # Allow access if user is invited
        if request.user in obj.invited_users.all():
            return True

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user
