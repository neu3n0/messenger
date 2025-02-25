from rest_framework import serializers
from .models import Chat, Participant, Message, ChannelSettings


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = (
            "id",
            "chat",
            "user",
            "role",
            "joined_at",
            "invitation_status",
            "is_blocked",
        )
        read_only_fields = (
            "id",
            "joined_at",
        )


class LastMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = (
            "id",
            "content",
            "created_at",
            "sender_username",
        )
        read_only_fields = fields


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "sender",
            "sender_username",
            "content",
            "created_at",
            "is_read",
            "is_edited",
        )
        read_only_fields = (
            "id",
            "created_at",
            "is_edited",
        )


class ChannelSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelSettings
        fields = (
            "is_public",
            "is_paid",
            "monthly_price",
        )
        read_only_fields = fields


class ChatListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    channel_settings = ChannelSettingsSerializer(
        source="channel_settings", read_only=True, allow_null=True
    )

    def get_last_message(self, obj):
        if obj.last_message:
            return LastMessageSerializer(obj.last_message).data
        return None

    class Meta:
        model = Chat
        fields = (
            "id",
            "chat_type",
            "title",
            "last_message",
            "channel_settings",
        )
        read_only_fields = fields


class ChatSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(
        many=True, read_only=True, source="chat_participants"
    )
    channel_settings = ChannelSettingsSerializer(
        source="channel_settings", read_only=True, allow_null=True
    )

    class Meta:
        model = Chat
        fields = (
            "id",
            "chat_type",
            "title",
            "description",
            "participants",
            "created_at",
            "channel_settings",
        )
        read_only_fields = (
            "id",
            "created_at",
        )
