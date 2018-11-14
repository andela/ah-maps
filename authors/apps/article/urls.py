from django.urls import path
from .views import (
    AddReaderAPIView
)

urlpatterns = [
    path('add', AddReaderAPIView.as_view(), name='read'),
]
