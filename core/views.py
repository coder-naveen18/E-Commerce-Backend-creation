from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.utils import timezone
from django.conf import settings


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            # Check if already verified
            if user.email_verified:
                return Response({'detail': 'Email already verified.'}, status=status.HTTP_200_OK)
            
            # Check if the token is expired (e.g., valid for 24 hours)
            expiry_hours = getattr(settings, 'VERIFICATION_TOKEN_EXPIRY', 48)
            

            token_age = timezone.now() - user.token_created_at

            if token_age.total_seconds() > (expiry_hours * 3600):  
                return Response({'detail': 'Verification token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            user.email_verified = True
            user.email_verification_token = None  # Invalidate the token after verification
            user.token_created_at = None
            user.save(update_fields=['email_verified', 'email_verification_token', 'token_created_at'])
            return Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)
