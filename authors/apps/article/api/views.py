from django.db.models import Q
from rest_framework.generics import (
  ListAPIView, CreateAPIView,
  RetrieveUpdateAPIView,
  RetrieveAPIView,
  DestroyAPIView
)
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly
)
from .serializers import TABLE, ArticleSerializer, ArticleCreateSerializer
from ...core.permissions import IsOwnerOrReadOnly

LOOKUP_FIELD = 'slug'


class ArticleListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ArticleSerializer

    def get_queryset(self, *args, **kwargs):
        """get all articles"""
        queryset_list = TABLE.objects.all()

        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(description__icontains=query)
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
