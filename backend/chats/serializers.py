from rest_framework import serializers
from .models import Chat, Participant, Message, ChannelSettings
from users.models import User
from django.db.models import Q, Count


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


class ChannelSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelSettings
        fields = (
            "is_public",
            "is_paid",
            "monthly_price",
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
            "is_read",
        )
        read_only_fields = fields


class ChatListSerializer(serializers.ModelSerializer):
    last_message = LastMessageSerializer(read_only=True, allow_null=True)
    channel_settings = ChannelSettingsSerializer(read_only=True, allow_null=True)
    title = serializers.SerializerMethodField()

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

    def get_title(self, obj):
        request = self.context.get("request")
        return obj.get_title(request.user)


class ChatCreateSerializer(serializers.ModelSerializer):
    channel_settings = ChannelSettingsSerializer(required=False)
    new_participants = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
        write_only=True,
        required=False,
    )
    participants = ParticipantSerializer(
        source="chat_participants",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Chat
        fields = (
            "id",
            "chat_type",
            "title",
            "description",
            "new_participants",
            "created_at",
            "channel_settings",
            "participants",
        )
        read_only_fields = (
            "id",
            "created_at",
            "participants",
        )

    def validate(self, attrs):
        chat_type = attrs.get("chat_type")
        new_participants = attrs.get("new_participants", [])
        user = self.context.get("request").user
        if chat_type == "direct":
            if len(new_participants) != 1:
                raise serializers.ValidationError(
                    {
                        "new_participants": "Direct chats require exactly one additional participant."
                    }
                )
            if new_participants[0].id == user.id:
                raise serializers.ValidationError(
                    {
                        "new_participants": "You cannot add yourself as a participant in a direct chat."
                    }
                )

            existing = (
                Chat.objects.filter(
                    chat_type="direct",
                    chat_participants__user=user,
                )
                .filter(chat_participants__user=new_participants[0])
                .exists()
            )
            print(user)
            print(new_participants[0])
            print(existing)

            if existing:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "A direct chat with this participant already exists."
                    }
                )

            attrs["title"] = (
                f"direct_chat_{user.username}_and_{new_participants[0].username}"
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        chat_type = validated_data.get("chat_type")
        new_participants_data = validated_data.pop("new_participants", [])
        channel_settings_data = validated_data.pop("channel_settings", {})

        chat = Chat.objects.create(**validated_data)

        if chat_type == "direct":
            chat.add_participant(user, role="member", invitation_status="accepted")
            chat.add_participant(
                new_participants_data[0], role="member", invitation_status="accepted"
            )
        elif chat_type == "group":
            chat.add_participant(user, role="admin", invitation_status="accepted")
            for participant in new_participants_data:
                if participant.id != user.id:
                    chat.add_participant(
                        participant, role="member", invitation_status="accepted"
                    )
        elif chat_type == "channel":
            chat.add_participant(user, role="admin", invitation_status="accepted")
            settings = ChannelSettings.objects.create(
                chat=chat, **channel_settings_data
            )
            inv_status = "accepted" if settings.is_public else "pending"
            for participant in new_participants_data:
                if participant.id != user.id:
                    chat.add_participant(
                        participant,
                        role="subscriber",
                        invitation_status=inv_status,
                    )

        return chat


class ChatSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(
        source="chat_participants",
        many=True,
        read_only=True,
    )
    channel_settings = ChannelSettingsSerializer(required=False, allow_null=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "chat_type",
            "title",
            "description",
            "created_at",
            "participants",
            "channel_settings",
        )
        read_only_fields = (
            "id",
            "chat_type",
            "created_at",
            "participants",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.chat_type == "direct":
            request = self.context.get("request")
            ret["title"] = instance.get_title(request.user)
        return ret

    def validate(self, attrs):
        if self.instance.chat_type != "channel" and attrs.get("channel_settings"):
            raise serializers.ValidationError(
                {
                    "channel_settings": "Channel settings can only be provided for channel chats."
                }
            )
        # if self.instance.chat_type == "direct" and attrs.get("title"):
        #     raise serializers.ValidationError(
        #         {"title": "Title can't be provided for direct chats."}
        #     )
        return attrs

    def update(self, instance, validated_data):
        channel_settings_data = validated_data.pop("channel_settings", None)
        if instance.chat_type == "channel" and channel_settings_data:
            for attr, value in channel_settings_data.items():
                setattr(instance.channel_settings, attr, value)
            instance.channel_settings.save()
        return super().update(instance, validated_data)
