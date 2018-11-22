from django.urls import path
from .views import (
    LikeCommentUpdateAPIView,
    DisLikeCommentUpdateAPIView
)


urlpatterns = [
    path(
        '<int:pk>/like',
        LikeCommentUpdateAPIView.as_view(),
        name='like'
    ),
    path(
        '<int:pk>/dislike',
        DisLikeCommentUpdateAPIView.as_view(),
        name='dislike'
    ),
]
