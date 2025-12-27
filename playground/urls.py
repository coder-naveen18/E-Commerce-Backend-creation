from django.urls import path
from .views import product, sendEmail

urlpatterns = [
    path('hello/', product),
    path('email/', sendEmail),
]
