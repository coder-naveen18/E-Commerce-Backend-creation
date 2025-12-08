from django.urls import path
from .views import firstlike
urlpatterns = [
    path('firstlike/', firstlike)
]
