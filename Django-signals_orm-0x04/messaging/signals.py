from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        print("🚨 Signal triggered: creating notification")
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}."
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is None:
        return  # New message, not an update

    try:
        original = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=original.content
        )
        instance.edited = True
