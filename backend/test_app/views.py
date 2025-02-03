from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import TestApp
from .serializers import TestAppSerializer

class TestAppRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer

class TestAppListCreateView(ListCreateAPIView):
    queryset = TestApp.objects.all()
    serializer_class = TestAppSerializer
