from django.shortcuts import render
# accounts/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
from .serializers import UserRegistrationSerializer
from .utils import email_verification_token
from .models import User
from rest_framework.permissions import AllowAny

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Allow unauthenticated users to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Registration successful. Please check your email to verify your account."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get uid and token from the URL query parameters
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')

        if not uid or not token:
            return Response({"error": "Missing parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Retrieve the user
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Validate the token
        if email_verification_token.check_token(user, token):
            # Token is valid, activate the user
            user.is_active = True
            user.save()
            
            # TODO: In a real app, redirect to a success page here
            return Response({"message": "Email successfully verified. You can now log in."}, status=status.HTTP_200_OK)
        else:
            # Token is invalid or expired
            return Response({"error": "The verification link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)