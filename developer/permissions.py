from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings

class IsDeveloper(BasePermission):
  """
    Custom permission to only allow developers to access developer-only views.
    """
  def has_permission(self, request, view):
      token = request.headers.get('Authorization')
      
      if not token:
          return False

      try:
          token = token.split(' ')[1]
          payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
          role = payload.get('role')

          return role == 'developer'
      except jwt.ExpiredSignatureError:
          return False
      except jwt.InvalidTokenError:
          return False