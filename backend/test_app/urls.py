from django.urls import path
from .views import TestAppListCreateView, TestAppRetrieveUpdateDestroyView

urlpatterns = [
    path('', TestAppListCreateView.as_view(), name='test_app-list-create'),
    path('<int:pk>/', TestAppRetrieveUpdateDestroyView.as_view(), name='test_app-retrieve-update-destroy'),
]
