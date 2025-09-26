from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Expose JWT views for urls.py
__all__ = [
    "TokenObtainPairView",
    "TokenRefreshView",
]
