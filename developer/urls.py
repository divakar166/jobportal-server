from django.urls import path
from .views import RegisterView, LoginView, DeveloperVerifyToken

urlpatterns = [
  path('register/', RegisterView.as_view(), name='developer-register'),
  path('login/', LoginView.as_view(), name='developer-login'),
  path('verify-token', DeveloperVerifyToken.as_view(), name='developer-verify-token')
]