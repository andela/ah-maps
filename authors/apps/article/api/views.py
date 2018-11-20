"""Articles api Views."""

from django.db.models import Q
from rest_framework import pagination
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView
)
from django.apps import apps
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
)
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers import (TABLE, ArticleSerializer,
                          ArticleCreateSerializer, ListLikersArticleSerializer,
                          ListDislikersArticleSerializer, ReportedArticleSerializer)
from ...core.permissions import IsOwnerOrReadOnly
from ...core.pagination import PostLimitOffsetPagination


LOOKUP_FIELD = 'slug'
PAGE_SIZE_KEY = 'page_size'
SEARCH_QUERY_PARAMETER = 'q'
SEARCH_BY_TAG = 'tag'
SEARCH_BY_AUTHOR = 'author'

Profile = apps.get_model('profile', 'Profile')
TAG = apps.get_model('tags', 'Tag')


def get_article(slug):
    """Get an article from the provided slug."""
    try:
        article = TABLE.objects.get(slug=slug)
        return article
    except TABLE.DoesNotExist:
        raise serializers.ValidationError(
            "Slug does not contain any matching article.")


class ArticleListAPIView(ListAPIView):
    """Artice list APIView."""

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        """get all articles"""
        self.serializer_class(context={'requet': kwargs.get('request')})
        queryset_list = TABLE.objects.all()

        page_size = self.request.GET.get(PAGE_SIZE_KEY)
        query = self.request.GET.get(SEARCH_QUERY_PARAMETER)
        tag = self.request.GET.get(SEARCH_BY_TAG)
        author = self.request.GET.get(SEARCH_BY_AUTHOR)
        pagination.PageNumberPagination.page_size = page_size if page_size else 10

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                | Q(description__icontains=query)
            )
        if tag:
            queryset_list = queryset_list.filter(
                Q(tags__tag__icontains=tag)  
            )
        if author:
             queryset_list = queryset_list.filter(
                Q(user__username__icontains=author)  
            )

        return queryset_list.order_by('-id')


class ArticleCreateAPIView(CreateAPIView):
    """create article"""
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = TABLE.objects.all()

    def perform_create(self, serializer):
        """create article"""
        serializer.save(user=self.request.user)


class ArticleDetailAPIView(RetrieveAPIView):
    """check article details"""
    permission_classes = [IsAuthenticated]
    queryset = TABLE.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = LOOKUP_FIELD


class ArticleDeleteAPIView(DestroyAPIView):
    """delete an article"""
    queryset = TABLE.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ArticleSerializer
    lookup_field = LOOKUP_FIELD


class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    """update an article"""
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TABLE.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = LOOKUP_FIELD

    def perform_update(self, serializer):
        """update an article"""
        serializer.save(user=self.request.user)


class LikeArticleAPIView(RetrieveUpdateDestroyAPIView):
    """Like article."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        """Like an article."""
        article = get_article(slug)
        username = request.user.username
        try:
            article.disliked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            article.undislike_article(request.user.profile)
        except Profile.DoesNotExist:
            pass
        # Check if the article has been liked before
        try:
            article.liked_by.get(user__username__exact=username)
            # If it has been liked before unlike it
            article.unlike_article(request.user.profile)
            message = {"success": "Like cancelled successfully."}
            return Response(message, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            # If it has not been liked before like it
            article.like_article(request.user.profile)
            message = {"success": "Article liked successfully."}
            return Response(message, status=status.HTTP_200_OK)


class DislikeArticleAPIView(RetrieveUpdateDestroyAPIView):
    """Dislike article."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        """Dislike an article."""
        article = get_article(slug)
        username = request.user.username
        # Check if the article has been disliked before
        try:
            article.liked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            article.unlike_article(request.user.profile)
        except Profile.DoesNotExist:
            pass

        try:
            article.disliked_by.get(user__username__exact=username)
            # If it has been disliked before undislike it
            article.undislike_article(request.user.profile)
            message = {"success": "Dislike cancelled successfully."}
            return Response(message, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            # If it has not been disliked before dislike it
            article.dislike_article(request.user.profile)
            message = {"success": "Article disliked successfully."}
            return Response(message, status=status.HTTP_200_OK)


class ListLikersArticleAPIView(RetrieveAPIView):
    """List users who like an article."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListLikersArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        """Overide get queryset."""
        queryset_list = TABLE.objects.all()

        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                | Q(description__icontains=query)
            )

        return queryset_list.order_by('-id')


class ListDislikersArticleAPIView(RetrieveAPIView):
    """List users who dislike an article."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListDislikersArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        """Overide get queryset."""
        queryset_list = TABLE.objects.all()

        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                | Q(slug__icontains=query)
                | Q(description__icontains=query)
            )

        return queryset_list.order_by('-id')


class ReportedArticleListAPIView(ListAPIView):
    """Artice list APIView."""

    permission_classes = [IsAdminUser]
    serializer_class = ReportedArticleSerializer
    queryset = TABLE.objects.filter(reports__isnull=False).distinct()

