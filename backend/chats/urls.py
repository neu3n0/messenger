from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ChatListCreateView,
    # ChatRetrieveUpdateDestroyView,
    MessageListCreateView,
    MessageRetrieveUpdateDestroyView,
    InviteUserView,
    AcceptInviteView,
    RejectInviteView,
    LeaveChatView,
    BlockUserView,
    UnblockUserView,
    ChatViewSet,
)

router = DefaultRouter()
router.register(r"", ChatViewSet, basename="chat")

urlpatterns = [
    # Чаты
    path("", include(router.urls)),
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
    # Выход
    path("<int:chat_id>/leave/", LeaveChatView.as_view(), name="chat-leave"),
    # Блокировка
    path("<int:chat_id>/block/", BlockUserView.as_view(), name="chat-block"),
    path("<int:chat_id>/unblock/", UnblockUserView.as_view(), name="chat-unblock"),
]
