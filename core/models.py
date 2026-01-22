import uuid 
from django.db import models
from django.contrib.auth.models import AbstractUser

def generate_uuid_hex():
    return uuid.uuid4().hex  # 32 chars, no hyphens
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=32, default=generate_uuid_hex, blank=True, editable=False, null=True)
    token_created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)