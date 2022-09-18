from rest_framework import serializers
from .models import RegistrationDetails


class RegistrationDetailsSerializer(serializers.Serializer):
    full_names = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    
    def create(self, validated_data):
        return RegistrationDetails.objects.create(**validated_data)