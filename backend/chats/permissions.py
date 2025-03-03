from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Participant


class IsAcceptedParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        chat = obj
        try:
            participant = chat.chat_participants.get(user=request.user)
        except Participant.DoesNotExist:
            return False
        return participant.invitation_status == "accepted"


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        chat = obj
        try:
            participant = chat.chat_participants.get(user=request.user)
        except Participant.DoesNotExist:
            return False
        return participant.role == "admin"


class IsAdminOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        chat = obj
        try:
            participant = chat.chat_participants.get(user=request.user)
        except Participant.DoesNotExist:
            return False
        return participant.role in ("admin", "moderator")


class IsMessageSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class CanDeleteMessage(BasePermission):
    def has_object_permission(self, request, view, obj):
        chat_type = obj.chat.chat_type
        if chat_type == "direct":
            return obj.sender == request.user
        else:
            if obj.sender == request.user:
                return True
            try:
                participant = obj.chat.chat_participants.get(user=request.user)
            except Participant.DoesNotExist:
                return False
            return participant.role in ("admin", "moderator")
