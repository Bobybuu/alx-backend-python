from django.urls import path, include
from rest_framework import routers

from .views import ConversationViewSet, MessageViewSet, UserViewSet
from rest_framework_extensions.routers import NestedDefaultRouter

# Note: NestedDefaultRouter is available for nested routing if needed

# Create a router and register our viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]