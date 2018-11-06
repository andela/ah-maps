from django.urls import path
from .views import (
   ProfileListAPIView,
   ProfileDetailAPIView,
   ProfileUpdateAPIView,
   ProfileListAPIView,
   MyProfileDetailAPIView
)

urlpatterns = [
    path('all/',ProfileListAPIView.as_view(), name='list'),
    path('me/', MyProfileDetailAPIView.as_view(), name='myprofile'),
    path('<user__username>/', ProfileDetailAPIView.as_view(), name='detail'),
    path('update/<user__username>/', ProfileUpdateAPIView.as_view(), name='update')
]
