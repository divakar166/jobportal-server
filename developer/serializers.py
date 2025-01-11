from rest_framework import serializers
from .models import Developer
from django.contrib.auth.hashers import make_password

class DeveloperSerializer(serializers.ModelSerializer):
  class Meta:
    model = Developer
    fields = ['id', 'name', 'email', 'mobile', 'image', 'password', 'created_at', 'updated_at']
    read_only_fields = ['id', 'created_at', 'updated_at']
    extra_kwargs = {
      'password': {'write_only': True},
      'email': {'required': True},
      'name': {'required': True}
    }