# accounts/utils.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# Custom token generator for email verification
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates a unique token based on the user's pk, timestamp, and is_active status.
    If any of these change, the token becomes invalid.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + 
            text_type(user.is_active) 
        )

# Instantiate the custom token generator
email_verification_token = EmailVerificationTokenGenerator()