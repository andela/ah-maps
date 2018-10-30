from django.urls import path
from .views import (
   ProfileListAPIView,
   ProfileDetailAPIView,
   ProfileUpdateAPIView
)

urlpatterns = [
    path('', ProfileListAPIView.as_view(), name='list'),
    path('<user__username>/', ProfileDetailAPIView.as_view(), name='detail'),
    path('update/<user__username>/', ProfileUpdateAPIView.as_view(), name='update')
]
