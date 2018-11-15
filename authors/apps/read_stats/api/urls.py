"""The read article urls."""

from django.urls import path
from .views import AddReaderAPIView, GetMyReadsAPIView

urlpatterns = [
    path('add/<slug>/', AddReaderAPIView.as_view(), name='read'),
    path('mine/', GetMyReadsAPIView.as_view(), name='my_reads'),
]
