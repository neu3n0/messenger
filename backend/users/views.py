from rest_framework import generics
from .serializers import UserSerializer


class UserRetrieveApiView(generics.RetrieveAPIView):
    """
    GET /api/profile/ - получение информации пользователя
    """

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
