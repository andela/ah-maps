"""Bookmark app endpoints."""

from django.urls import path
from .views import (
   BookMarkListAPIView,
   BookMarkArticleAPIView,
)


urlpatterns = [
    path('add/<slug>/', BookMarkArticleAPIView.as_view(), name='add'),
    path('remove/<slug>/', BookMarkArticleAPIView.as_view(), name='remove'),
    path('mine/', BookMarkListAPIView.as_view(), name='list')
]
