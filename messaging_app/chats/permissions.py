from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated participants of a conversation 
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users can access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Ensure that only participants can access objects.
        Explicitly restrict GET, POST, PUT, PATCH, DELETE to participants.
        """
        if isinstance(obj, Conversation):
            participants = obj.participants.all()
        elif isinstance(obj, Message):
            participants = obj.conversation.participants.all()
        else:
            return False

        #  Allow only participants for all critical methods
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in participants

        # Allow safe methods (HEAD, OPTIONS) by default
        return True
