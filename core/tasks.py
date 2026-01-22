from celery import shared_task
from django.conf import settings
from .models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import os


@shared_task
def send_verification_email(user_id, email, token):
    try:
        user = get_object_or_404(User, id=user_id)
        subject = 'Verify your email address'
        # Direct backend verification (no frontend needed for testing)
        verification_url = f"http://localhost:8000/core/verify-email/{token}/"
        message = render_to_string('core/emails/email_verification.html', {
            'user': user,
            'token': token,
            'verification_url': verification_url,
            'verification_expiry': getattr(settings, 'VERIFICATION_TOKEN_EXPIRY', 48)
        })
        send_mail(
        subject=subject,
        message='',  # Plain text version (can be empty if using HTML)
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=message  # This is where the HTML goes
        )
    except Exception as e:
        print(f"Failed to send verification email to {email}: {e}")