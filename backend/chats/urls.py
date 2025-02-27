from django.urls import path
from .views import (
    ChatListCreateView,
    ChatRetrieveUpdateDestroyView,
    MessageListCreateView,
    MessageRetrieveUpdateDestroyView,
    InviteUserView,
    AcceptInviteView,
    RejectInviteView,
    LeaveChatView,
    BlockUserView,
    UnblockUserView,
)

urlpatterns = [
    # Чаты
    path("", ChatListCreateView.as_view(), name="chat-list-create"),
    path("<int:pk>/", ChatRetrieveUpdateDestroyView.as_view(), name="chat-detail"),
    # Сообщения (вложенный ресурс: /chats/<chat_id>/messages/)
    path(
        "<int:chat_id>/messages/",
        MessageListCreateView.as_view(),
        name="message-list-create",
    ),
    path(
        "<int:chat_id>/messages/<int:pk>/",
        MessageRetrieveUpdateDestroyView.as_view(),
        name="message-detail",
    ),
    # Приглашения
    path("<int:chat_id>/invite/", InviteUserView.as_view(), name="chat-invite"),
    path(
        "<int:chat_id>/invite/accept/",
        AcceptInviteView.as_view(),
        name="chat-invite-accept",
    ),
    path(
        "<int:chat_id>/invite/reject/",
        RejectInviteView.as_view(),
        name="chat-invite-reject",
    ),
    # Выход
    path("<int:chat_id>/leave/", LeaveChatView.as_view(), name="chat-leave"),
    # Блокировка
    path("<int:chat_id>/block/", BlockUserView.as_view(), name="chat-block"),
    path("<int:chat_id>/unblock/", UnblockUserView.as_view(), name="chat-unblock"),
]
