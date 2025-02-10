from django.db import models
from users.models import User


class Chat(models.Model):
    """
    Chat model
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
        User, through="Participant", related_name="chats", verbose_name="Participants"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Message(models.Model):
    """
    Message model
    """

    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages", verbose_name="Chat"
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
    Participant model
    """

    ROLE_TYPE_CHOICES = [
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("member", "Member"),
        ("subscriber", "Subscriber"),
    ]

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
        max_length=20, choices=ROLE_TYPE_CHOICES, default="member", verbose_name="Role"
    )

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        unique_together = (("chat", "user"),)
