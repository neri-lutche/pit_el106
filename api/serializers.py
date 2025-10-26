# accounts/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from .models import User
from .utils import email_verification_token # Import the token generator
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # 1. Check if passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # 2. Basic email validation
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})
            
        return data

    def create(self, validated_data):
        # Remove the extra 'password2' field
        validated_data.pop('password2')
        
        # Create user (is_active=False by default, handled in the User Manager)
        user = User.objects.create_user(**validated_data)
        
        # --- Email Verification Logic ---
        token = email_verification_token.make_token(user)
        relative_link = reverse('verify-email') # URL name for the verification endpoint

        # Build the complete verification URL
        verification_link = f"{settings.SITE_URL}{relative_link}?uid={user.pk}&token={token}"
        
        # Email content
        email_body = f"""
        Hi {user.first_name},

        Thank you for registering. Please click on the link below to verify your email address:
        {verification_link}

        If you did not register for this service, please ignore this email.
        """
        email = EmailMessage(
            subject='Verify Your Email Address',
            body=email_body,
            to=[user.email]
        )
        email.send()
        
        return user

# --- Custom JWT Serializer to enforce is_active=True on login ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Check if the user is active (verified) before generating tokens
        if not user.is_active:
             raise serializers.ValidationError("Account not verified. Please check your email.")
             
        # Generate token if user is active
        token = super().get_token(user)

        # Add custom claims (optional but useful)
        token['username'] = user.username
        token['email'] = user.email

        return token