from django.urls import path
from .views import (
   CommentCreateAPIView,
   CommentListAPIView,
   CommentDeleteAPIView,
   CommentDetailAPIView,
   CommentUpdateAPIView
)

urlpatterns = [
    path('<slug>/', CommentListAPIView.as_view(), name='list'),
    path('<slug>/comment/', CommentCreateAPIView.as_view(), name='comment'),
    path('<slug>/comment/<int:pk>', CommentCreateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', CommentDeleteAPIView.as_view(), name='delete'),
    path('detail/<int:pk>/', CommentDetailAPIView.as_view(), name='detail'),
    path('<slug>/<int:pk>/', CommentUpdateAPIView.as_view(), name='thread'),
    path('update/<int:pk>/', CommentUpdateAPIView.as_view(), name='update'),
]
