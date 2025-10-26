# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegistrationView, EmailVerificationView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView # Use the built-in view

urlpatterns = [
    # 1. User Registration (Public)
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # 2. Login Functionality (Public) - Simple JWT Token Obtain
    path('login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    
    # 3. Token Refresh (Public) - Get a new Access Token using the Refresh Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 4. Email Verification (Public - accessed via GET link)
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
]