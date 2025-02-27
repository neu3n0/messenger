from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Chat, Message, Participant
from .serializers import (
    ChatListSerializer,
    ChatCreateSerializer,
    ChatSerializer,
    MessageSerializer,
)


class ChatListCreateView(generics.ListCreateAPIView):
    """
    GET /api/chats/:
      - Returns a list of chats (direct, group, channel) where the user's invitation_status is accepted or pending
      - Uses ChatListSerializer
      - Chats are ordered by -last_message_time, then by -id

    POST /api/chats/:
      - Creates a new chat (direct, group, channel)
      - Uses ChatSerializer
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Chat.objects.filter(
                chat_participants__user=self.request.user,
                chat_participants__invitation_status__in=["accepted", "pending"],
            )
            .select_related("channel_settings", "last_message")
            .order_by("-last_message_time", "-id")
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatListSerializer
        return ChatCreateSerializer

    def perform_create(self, serializer):
        serializer.context["request"] = self.request
        serializer.save()


class ChatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/chats/<pk>/:
      - Returns detailed information about a chat (using ChatSerializer).
      - If the user's invitation_status is pending, a trimmed representation (without description and participants) is returned.

    PATCH/PUT /api/chats/<pk>/:
      - Only (admin | moderator) & accepted.

    DELETE /api/chats/<pk>/:
      - Only admin & accepted.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(
            chat_participants__user=self.request.user,
            chat_participants__invitation_status__in=["accepted", "pending"],
        )

    def retrieve(self, request, *args, **kwargs):
        chat = self.get_object()
        participant = get_object_or_404(Participant, chat=chat, user=request.user)
        if participant.invitation_status == "pending":
            # If invitation status is pending, return a trimmed version
            data = {
                "id": chat.id,
                "chat_type": chat.chat_type,
                "title": chat.title,
            }
            return Response(data, status=status.HTTP_200_OK)
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        chat = self.get_object()
        if chat.chat_type == "direct":
            raise PermissionDenied("Direct chats cannot be updated.")
        participant = Participant.objects.get(chat=chat, user=self.request.user)
        if participant.invitation_status != "accepted" or participant.role not in [
            "admin",
            "moderator",
        ]:
            raise PermissionError("You do not have permission to update this chat.")
        serializer.save()

    def perform_destroy(self, instance):
        participant = Participant.objects.get(chat=instance, user=self.request.user)
        if participant.invitation_status != "accepted" or participant.role != "admin":
            raise PermissionError("You do not have permission to delete this chat.")
        instance.delete()


#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
#################################
class MessageListCreateView(generics.ListCreateAPIView):
    """
    GET /api/chats/<chat_id>/messages/:
    - Returns a list of messages in the specified chat (accepted & is_blocked=False).

    POST /api/chats/<chat_id>/messages/:
      - Creates a new message.
      - After creation, updates chat.last_message and chat.last_message_time.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        # Ensure the user is a participant with accepted status and not blocked.
        chat = get_object_or_404(
            Chat,
            pk=chat_id,
            chat_participants__user=self.request.user,
            chat_participants__invitation_status="accepted",
            chat_participants__is_blocked=False,
        )
        return Message.objects.filter(chat=chat)

    def perform_create(self, serializer):
        chat_id = self.kwargs.get("chat_id")
        chat = get_object_or_404(
            Chat,
            pk=chat_id,
            chat_participants__user=self.request.user,
            chat_participants__invitation_status="accepted",
            chat_participants__is_blocked=False,
        )
        message = serializer.save(chat=chat, sender=self.request.user)

        # Update last_message, last_message_time
        chat.last_message = message
        chat.last_message_time = message.created_at
        chat.save(update_fields=["last_message", "last_message_time"])


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/chats/<chat_id>/messages/<pk>/:
      - Returns detailed information about a specific message (accepted & not blocked)

    PATCH/PUT:
      - Allows update if the user is the sender

    DELETE:
      - Deletes the message.
      - If the deleted message was chat.last_message, recalculates a new last message.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        return Message.objects.filter(
            chat__id=chat_id,
            chat__chat_participants__user=self.request.user,
            chat__chat_participants__invitation_status="accepted",
            chat__chat_participants__is_blocked=False,
        )

    def perform_update(self, serializer):
        message = self.get_object()
        if message.sender == self.request.user:
            serializer.save(is_edited=True)
        else:
            raise PermissionError("You do not have permission to edit this message.")

    def perform_destroy(self, instance):
        participant = Participant.objects.get(
            chat=instance.chat, user=self.request.user
        )
        # Allow deletion if the user is the sender or is admin/moderator.
        if instance.sender == self.request.user or participant.role in [
            "admin",
            "moderator",
        ]:
            chat = instance.chat
            message_id = instance.id
            instance.delete()

            # Update last message if its neccesary
            if chat.last_message_id == message_id:
                new_last = chat.messages.order_by("-created_at").first()
                chat.last_message = new_last
                chat.last_message_time = new_last.created_at if new_last else None
                chat.save(update_fields=["last_message", "last_message_time"])
        else:
            raise PermissionError("You do not have permission to delete this message.")


# ========================== INVITE / ACCEPT / REJECT / LEAVE / BLOCK ==========================


class InviteUserView(APIView):
    """
    POST /api/chats/<chat_id>/invite/:
      - Только admin (accepted).
      - Создаём participant со статусом 'pending' (если group/channel).
      - Не для direct.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        from users.models import User

        chat = get_object_or_404(Chat, pk=chat_id)
        admin_participant = get_object_or_404(
            Participant, chat=chat, user=request.user, invitation_status="accepted"
        )
        if admin_participant.role != "admin":
            return Response(
                {"detail": "Only admin can invite."}, status=status.HTTP_403_FORBIDDEN
            )

        if chat.chat_type == "direct":
            return Response(
                {"detail": "Cannot invite to direct chat."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)

        invitee = get_object_or_404(User, pk=user_id)

        if Participant.objects.filter(chat=chat, user=invitee).exists():
            return Response({"detail": "User already in chat or invited."}, status=400)

        role = request.data.get("role", "member")
        if chat.chat_type == "channel":
            role = "subscriber"

        Participant.objects.create(
            chat=chat, user=invitee, role=role, invitation_status="pending"
        )
        return Response({"detail": "User invited (pending)."}, status=201)


class AcceptInviteView(APIView):
    """
    POST /api/chats/<chat_id>/invite/accept/:
      - Пользователь (pending) => accepted.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        participant = get_object_or_404(
            Participant, chat=chat, user=request.user, invitation_status="pending"
        )
        participant.invitation_status = "accepted"
        participant.save()
        return Response({"detail": "Invitation accepted."}, status=200)


class RejectInviteView(APIView):
    """
    POST /api/chats/<chat_id>/invite/reject/:
      - pending => rejected.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        participant = get_object_or_404(
            Participant, chat=chat, user=request.user, invitation_status="pending"
        )
        participant.invitation_status = "rejected"
        participant.save()
        return Response({"detail": "Invitation rejected."}, status=200)


class LeaveChatView(APIView):
    """
    POST /api/chats/<chat_id>/leave/:
      - Удаляем запись participant (только если group/channel).
      - direct - нельзя уйти (логика по вашему усмотрению).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        if chat.chat_type == "direct":
            return Response({"detail": "Cannot leave a direct chat."}, status=400)

        participant = get_object_or_404(Participant, chat=chat, user=request.user)
        participant.delete()
        return Response({"detail": "You have left the chat."}, status=200)


class BlockUserView(APIView):
    """
    POST /api/chats/<chat_id>/block/:
      - Заблокировать user_id.
      - group/channel: только admin/moderator
      - direct: любой из двух
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        from users.models import User

        chat = get_object_or_404(Chat, pk=chat_id)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)
        user_to_block = get_object_or_404(User, pk=user_id)

        current_participant = get_object_or_404(
            Participant,
            chat=chat,
            user=request.user,
            invitation_status="accepted",
            is_blocked=False,
        )
        blocked_participant = get_object_or_404(
            Participant, chat=chat, user=user_to_block
        )

        if chat.chat_type in ["group", "channel"]:
            if current_participant.role not in ["admin", "moderator"]:
                return Response({"detail": "No permission to block."}, status=403)
        # direct - любой может блокировать

        blocked_participant.is_blocked = True
        blocked_participant.save()
        return Response({"detail": f"User {user_id} blocked."}, status=200)


class UnblockUserView(APIView):
    """
    POST /api/chats/<chat_id>/unblock/:
      - Разблокировать user_id
      - group/channel: admin/moderator
      - direct: любой
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        from users.models import User

        chat = get_object_or_404(Chat, pk=chat_id)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id is required"}, status=400)
        user_to_unblock = get_object_or_404(User, pk=user_id)

        current_participant = get_object_or_404(
            Participant,
            chat=chat,
            user=request.user,
            invitation_status="accepted",
            is_blocked=False,
        )
        blocked_participant = get_object_or_404(
            Participant, chat=chat, user=user_to_unblock
        )

        if chat.chat_type in ["group", "channel"]:
            if current_participant.role not in ["admin", "moderator"]:
                return Response({"detail": "No permission to unblock."}, status=403)

        blocked_participant.is_blocked = False
        blocked_participant.save()
        return Response({"detail": f"User {user_id} unblocked."}, status=200)
