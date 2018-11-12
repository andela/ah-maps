from django.urls import path
from .views import (
    ArticleCreateAPIView,
    ArticleListAPIView,
    ArticleDeleteAPIView,
    ArticleDetailAPIView,
    ArticleUpdateAPIView,
    LikeArticleAPIView,
    DislikeArticleAPIView,
    ListLikersArticleAPIView,
    ListDislikersArticleAPIView
)

urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='list'),
    path('create', ArticleCreateAPIView.as_view(), name='create'),
    path('delete/<slug>/', ArticleDeleteAPIView.as_view(), name='delete'),
    path('detail/<slug>/', ArticleDetailAPIView.as_view(), name='detail'),
    path('update/<slug>/', ArticleUpdateAPIView.as_view(), name='update'),
    path('like/<slug>/', LikeArticleAPIView.as_view(), name='like'),
    path('dislike/<slug>/', DislikeArticleAPIView.as_view(), name='dislike'),
    path('liked/<slug>/', ListLikersArticleAPIView.as_view(), name='likers'),
    path('disliked/<slug>/', ListDislikersArticleAPIView.as_view(), name='dislikers'),
]
