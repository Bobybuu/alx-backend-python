from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):
    def test_notification_created_on_new_message(self):
        sender = User.objects.create_user(username='alice', password='1234')
        receiver = User.objects.create_user(username='bob', password='1234')

        Message.objects.create(sender=sender, receiver=receiver, content="Hello!")

        self.assertEqual(Notification.objects.filter(user=receiver).count(), 1)

