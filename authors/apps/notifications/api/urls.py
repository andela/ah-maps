"""Define the notifications urls."""

from django.urls import path
from .views import NotificationsListAPIView, NotificationsSubscriptionAPIView

urlpatterns = [
    path('<int:id>/', NotificationsListAPIView.as_view(), name='get_one'),
    path('', NotificationsListAPIView.as_view(), name='get_all'),
    path('subscribe/', NotificationsSubscriptionAPIView.as_view(), name='subscription'),
]
