from rest_framework import serializers

from .models import TestApp


class TestAppSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = TestApp
        fields = (
            "id",
            "arg1",
            "arg2",
            "owner",
        )
