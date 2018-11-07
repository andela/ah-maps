from django.urls import path
from .views import (
   ProfileListAPIView,
   ProfileDetailAPIView,
   ProfileUpdateAPIView,
   FollowProfilesAPIView,
   ListFollowingProfilesAPIView,
   ListFollowersProfilesAPIView,
   MyProfileDetailAPIView
)

urlpatterns = [
    path('all/',ProfileListAPIView.as_view(), name='list'),
    path('me/', MyProfileDetailAPIView.as_view(), name='myprofile'),
    path('<user__username>/', ProfileDetailAPIView.as_view(), name='detail'),
    path('update/<user__username>/', ProfileUpdateAPIView.as_view(), name='update'),
    path('<username>/follow', FollowProfilesAPIView.as_view(), name='follow_unfollow'),
    path('<username>/following', ListFollowingProfilesAPIView.as_view(), name='get_followed'),
    path('<username>/followers', ListFollowersProfilesAPIView.as_view(), name='get_followers'),
]
