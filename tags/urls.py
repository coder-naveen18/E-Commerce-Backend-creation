from django.urls import path
from .views import tags
urlpatterns = [
    path('firsttag/', tags)
]
