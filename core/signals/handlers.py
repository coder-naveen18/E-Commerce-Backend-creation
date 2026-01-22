from core.tasks import send_verification_email
from store.signals import order_created
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone
import uuid

@receiver(order_created)
def on_order_created(sender, **kwargs):
    # Example handler function for order_created signal
    print(kwargs['order'])

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_email_verification_on_signup(sender, instance, created, **kwargs):
    if created and not instance.email_verified:
        # generate token logic here
        instance.email_verification_token = uuid.uuid4().hex
        instance.token_created_at = timezone.now()
        instance.save(update_fields=['email_verification_token', 'token_created_at'])  
        send_verification_email.delay(instance.id, instance.email, instance.email_verification_token) 