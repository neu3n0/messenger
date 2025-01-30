from rest_framework import serializers

from .models import TestApp

class TestAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestApp
        fields = '__all__'