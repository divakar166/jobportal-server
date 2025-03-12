from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings

class IsRecruiter(BasePermission):
    """
    Custom permission to only allow recruiters to access recruiter-only views.
    """
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        
        if not token:
            return False

        try:
            # Extract the token and verify it
            token = token.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            role = payload.get('role')

            # Check if the role is 'recruiter'
            return role == 'recruiter'
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
