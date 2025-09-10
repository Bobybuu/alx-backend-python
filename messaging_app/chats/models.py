import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending AbstractUser with additional fields"""
    
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'
    
    # Replace the default ID with UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Additional fields beyond AbstractUser
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    # Override email field to make it unique and required
    email = models.EmailField(unique=True, blank=False, null=False)
    
    # Remove username field and use email as the username
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Conversation(models.Model):
    """Model representing a conversation between users"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        User, 
        related_name='conversations',
        through='ConversationParticipant'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        participant_names = [str(user) for user in self.participants.all()[:3]]
        return f"Conversation {self.id} - Participants: {', '.join(participant_names)}"


class ConversationParticipant(models.Model):
    """Through model for Conversation participants with additional metadata"""
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['conversation', 'user']
        indexes = [
            models.Index(fields=['conversation', 'user']),
        ]
    
    def __str__(self):
        return f"{self.user} in {self.conversation}"


class Message(models.Model):
    """Model representing a message in a conversation"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    message_body = models.TextField(blank=False, null=False)
    sent_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['sender', 'sent_at']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"