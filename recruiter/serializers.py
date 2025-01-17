from rest_framework import serializers
from .models import Recruiter
from django.contrib.auth.hashers import make_password

class RecruiterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Recruiter
    fields = ['id', 'name', 'email', 'mobile', 'image', 'password', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']
    extra_kwargs = {
      'password': {'write_only': True},
      'email': {'required': True},
      'name': {'required': True},
      'mobile': {'required': True}
    }