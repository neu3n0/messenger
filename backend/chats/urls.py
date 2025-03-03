from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ChatViewSet

router = DefaultRouter()
router.register(r"", ChatViewSet, basename="chat")

message_list = MessageViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
message_detail = MessageViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path("<int:chat_id>/messages/", message_list, name="message-list"),
    path("<int:chat_id>/messages/<int:pk>/", message_detail, name="message-detail"),
]
