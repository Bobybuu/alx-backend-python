from rest_framework import serializers
from .models import User, Conversation, Message, ConversationParticipant


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']
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
            'message_id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sender', 'sent_at']
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
            'conversation_id', 'participants', 'participant_ids', 
            'messages', 'message_count', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'participants', 'messages', 'message_count']
    
    def get_message_count(self, obj):
        """Get the count of messages in the conversation"""
        return obj.messages.count()
    
    def validate_participant_ids(self, value):
        """Custom validation for participant IDs"""
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value
    
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


# Additional serializers with CharField and ValidationError usage
class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating messages with validation"""
    
    message_body = serializers.CharField(
        max_length=1000,
        required=True,
        error_messages={
            'required': 'Message body is required.',
            'max_length': 'Message cannot exceed 1000 characters.'
        }
    )
    
    class Meta:
        model = Message
        fields = ['message_body', 'conversation', 'sender']
        read_only_fields = ['sender']
    
    def validate_message_body(self, value):
        """Custom validation for message body"""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value.strip()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating conversations with validation"""
    
    participant_ids = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        error_messages={
            'required': 'At least one participant ID is required.'
        }
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids']
    
    def validate_participant_ids(self, value):
        """Validate participant IDs"""
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required.")
        
        # Check if all participant IDs are valid
        valid_users = User.objects.filter(user_id__in=value)
        if len(valid_users) != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        
        return value