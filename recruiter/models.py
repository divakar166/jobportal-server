from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import jwt
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import now


class Recruiter(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255)
  email = models.EmailField(unique=True, db_index=True)
  mobile = models.CharField(max_length=15, unique=True)
  image = models.URLField(null=True, blank=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "recruiters"

  def __str__(self):
    return f"{self.name} ({self.email})"

  def set_password(self, raw_password):
    try:
      validate_password(raw_password)
    except ValidationError as e:
      raise ValueError("Password does not meet the strength requirements: " + ", ".join(e.messages))
    self.password = make_password(raw_password)

  def check_password(self, raw_password):
    return check_password(raw_password, self.password)

  def generate_token(self):
    payload = {
      'id': str(self.id),
      'email': self.email,
      'exp': datetime.utcnow() + timedelta(days=1),
      'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')