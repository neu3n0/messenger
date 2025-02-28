from django.db import models
from users.models import User
from decimal import Decimal


class Chat(models.Model):
    """
    Universal Chat model for direct, group, and channel chats
    The type of chat is determined by the chat_type field
    """

    CHAT_TYPE_CHOICES = (
        ("direct", "Direct Message"),
        ("group", "Group Chat"),
        ("channel", "Channel"),
    )

    chat_type = models.CharField(
        max_length=20,
        choices=CHAT_TYPE_CHOICES,
        default="direct",
        verbose_name="Chat Type",
    )
    title = models.CharField(max_length=255, verbose_name="Chat Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    participants = models.ManyToManyField(
        User,
        through="Participant",
        related_name="chats",
        verbose_name="Participants",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    # Fields to denormalise the last message
    last_message = models.ForeignKey(
        "Message",  # string to avoid cyclic dependency
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",  # no backward relation
        verbose_name="Last Message",
    )
    last_message_time = models.DateTimeField(
        null=True, blank=True, verbose_name="Last Message Time"
    )

    def get_title(self, current_user):
        if self.chat_type == "direct":
            participant = self.chat_participants.exclude(user=current_user).first()
            return participant.user.username if participant else "Unknown"
        return self.title

    def add_participant(self, user, role, invitation_status, is_blocked=False):
        participant, created = Participant.objects.get_or_create(
            chat=self,
            user=user,
            defaults={
                "role": role,
                "invitation_status": invitation_status,
                "is_blocked": is_blocked,
            },
        )
        if not created:
            updated = False
            if participant.role != role:
                participant.role = role
                updated = True
            if participant.invitation_status != invitation_status:
                participant.invitation_status = invitation_status
                updated = True
            if participant.is_blocked != is_blocked:
                participant.is_blocked = is_blocked
                updated = True
            if updated:
                participant.save()
        return participant

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Message(models.Model):
    """
    Message model - stores messages sent in a chat
    """

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Chat",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
        verbose_name="Sender",
    )
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    is_edited = models.BooleanField(default=False, verbose_name="is Edited")

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-created_at"]


class Participant(models.Model):
    """
    Participant model - links a user to a chat and stores their role,
    invitation status, and whether they are blocked
    The role field includes "admin", "moderator", "member", and "subscriber"
    "subscriber" is typically used in channels for read-only subscribers
    """

    ROLE_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("member", "Member"),
        ("subscriber", "Subscriber"),
    )
    INVITATION_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="chat_participants",
        verbose_name="Chat",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_participants",
        verbose_name="User",
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined At")
    role = models.CharField(
        max_length=20,
        choices=ROLE_TYPE_CHOICES,
        default="member",
        verbose_name="Role",
    )
    invitation_status = models.CharField(
        max_length=20,
        choices=INVITATION_STATUS_CHOICES,
        default="accepted",
        verbose_name="Invitation Status",
    )
    is_blocked = models.BooleanField(default=False, verbose_name="Is Blocked")

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        unique_together = (("chat", "user"),)


class ChannelSettings(models.Model):
    """
    ChannelSettings - stores additional settings for a channel.
    Linked via OneToOneField to a Chat object with chat_type = "channel".
    Fields:
      - is_public: True if channel is open, False if closed (only invited users can join).
      - is_paid: True if channel requires payment.
      - monthly_price: Price for subscription.
    """

    chat = models.OneToOneField(
        Chat,
        on_delete=models.CASCADE,
        related_name="channel_settings",
        verbose_name="Channel Settings",
    )
    is_public = models.BooleanField(default=True, verbose_name="Is Public")
    is_paid = models.BooleanField(default=False, verbose_name="Is Paid Channel")
    monthly_price = models.FloatField(default=0, verbose_name="Monthly Price")

    class Meta:
        verbose_name = "Channel Settings"
        verbose_name_plural = "Channel Settings"
