from django.db import models


# Product
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
