from django.urls import path
from .views import myname
urlpatterns = [
    path('first/', myname)
]
