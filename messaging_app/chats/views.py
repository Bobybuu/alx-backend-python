from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, 
    ConversationDetailSerializer,
    MessageSerializer,
    UserSerializer,
    MessageCreateSerializer,
    ConversationCreateSerializer
)
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model with custom actions"""
    
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        elif self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages').order_by('-created_at')
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add current user as participant
        ConversationParticipant = Conversation.participants.through
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=self.request.user
        )
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().select_related('sender')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if conversation.participants.filter(user_id=user_id).exists():
            return Response({'error': 'User already a participant'}, status=status.HTTP_400_BAD_REQUEST)
        
        ConversationParticipant = Conversation.participants.through
        ConversationParticipant.objects.create(conversation=conversation, user=user)
        
        return Response({'message': 'Participant added successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not conversation.participants.filter(user_id=user_id).exists():
            return Response({'error': 'User not a participant'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation.participants.remove(user_id)
        
        return Response({'message': 'Participant removed successfully'}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model - only conversation participants can CRUD"""
    
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').order_by('-sent_at')
    
    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        if conversation_id:
            # Ensure user is part of conversation
            get_object_or_404(
                Conversation,
                conversation_id=conversation_id,
                participants=self.request.user
            )
        serializer.save(sender=self.request.user)
    
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        
        if not conversation_id:
            return Response({'error': 'conversation field is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Conversation.objects.filter(conversation_id=conversation_id, participants=request.user).exists():
            return Response({'error': 'Conversation not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Allow only the sender to update their own message"""
        message = self.get_object()
        if message.sender != request.user:
            return Response({'error': 'You can only edit your own messages'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Allow only the sender to delete their own message"""
        message = self.get_object()
        if message.sender != request.user:
            return Response({'error': 'You can only delete your own messages'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model (read-only)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email']
    
    def get_queryset(self):
        return User.objects.exclude(user_id=self.request.user.user_id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def conversations(self, request, pk=None):
        user = self.get_object()
        if user != request.user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        conversations = user.conversations.all().prefetch_related('participants', 'messages')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
