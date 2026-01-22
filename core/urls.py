from django.views.generic import TemplateView
from django.urls import path
from .views import VerifyEmailView

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'core/index.html')),   
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]
