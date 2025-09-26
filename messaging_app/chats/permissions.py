from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated participants of a conversation 
    to view, create, update, or delete messages/conversations.
    """

    def has_permission(self, request, view):
        # Must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj may be a Conversation or a Message.
        """
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False
