from rest_framework import serializers
from .models import User, Conversation, Message, ConversationParticipant


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    
    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender',
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['id', 'sender', 'sent_at']
        extra_kwargs = {
            'conversation': {'required': True},
            'message_body': {'required': True},
        }


class ConversationParticipantSerializer(serializers.ModelSerializer):
    """Serializer for ConversationParticipant through model"""
    
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True,
        required=True
    )
    
    class Meta:
        model = ConversationParticipant
        fields = ['id', 'user', 'user_id', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested relationships"""
    
    participants = ConversationParticipantSerializer(
        source='conversationparticipant_set', 
        many=True, 
        read_only=True
    )
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=True,
        source='participants'
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'participant_ids', 
            'messages', 'message_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'participants', 'messages', 'message_count']
    
    def get_message_count(self, obj):
        """Get the count of messages in the conversation"""
        return obj.messages.count()
    
    def create(self, validated_data):
        """Create conversation and add participants"""
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        for participant in participants:
            ConversationParticipant.objects.create(
                conversation=conversation,
                user=participant
            )
        
        return conversation
    
    def update(self, instance, validated_data):
        """Update conversation participants"""
        participants = validated_data.pop('participants', None)
        
        if participants is not None:
            # Clear existing participants and add new ones
            instance.participants.clear()
            for participant in participants:
                ConversationParticipant.objects.create(
                    conversation=instance,
                    user=participant
                )
        
        return super().update(instance, validated_data)


class ConversationDetailSerializer(ConversationSerializer):
    """Detailed serializer for Conversation with full message details"""
    
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']


class UserWithConversationsSerializer(UserSerializer):
    """User serializer with nested conversations"""
    
    conversations = ConversationSerializer(many=True, read_only=True)
    conversation_count = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['conversations', 'conversation_count']
    
    def get_conversation_count(self, obj):
        """Get the count of conversations the user is in"""
        return obj.conversations.count()