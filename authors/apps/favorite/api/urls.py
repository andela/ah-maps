from django.urls import path
from .views import (
    FavoriteArticleUpdateAPIView,
    FavoriteArticleListAPIView
)


urlpatterns = [
    path('', FavoriteArticleListAPIView.as_view(), name='list'),
    path('<slug>/', FavoriteArticleUpdateAPIView.as_view(), name='update')
]
