from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import TestApp
from .serializers import TestAppSerializer
from .permissioins import IsOwnerOrReadOnly

class TestAppRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class TestAppListCreateView(ListCreateAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
