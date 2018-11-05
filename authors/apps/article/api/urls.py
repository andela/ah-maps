from django.urls import path
from .views import (
   ArticleCreateAPIView,
   ArticleListAPIView,
   ArticleDeleteAPIView,
   ArticleDetailAPIView,
   ArticleUpdateAPIView
)

urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='list'),
    path('create', ArticleCreateAPIView.as_view(), name='create'),
    path('delete/<slug>/', ArticleDeleteAPIView.as_view(), name='delete'),
    path('detail/<slug>/', ArticleDetailAPIView.as_view(), name='detail'),
    path('update/<slug>/', ArticleUpdateAPIView.as_view(), name='update')
]
