from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView,
    UserRetrieveUpdateAPIView, ActivateAPIView, ResetPasswordAPIView,
    UpdateUserAPIView, SocialSignUp
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="specific_user"),
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('user/activate/<str:token>', ActivateAPIView.as_view(), name="activate"),
    path('users/social_auth/', SocialSignUp.as_view(), name='social')
    path('user/resetpassword', ResetPasswordAPIView.as_view(), name="resetpassword"),
    path('user/update/<str:token>', UpdateUserAPIView.as_view(), name="updateuser"),
    path('users/social_auth/', SocialSignUp.as_view(), name='social'),
]
