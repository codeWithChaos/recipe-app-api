"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name'] # fields for the serializer model
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} # extra validation for the password

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data) # Overwriting the create method to pass in the validated data from the serializer
