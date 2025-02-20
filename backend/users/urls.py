from django.urls import path
from .views import UserRetrieveApiView

urlpatterns = [
    path(
        "",
        UserRetrieveApiView.as_view(),
        name="profile-detail",
    ),
]
