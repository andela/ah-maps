from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from .serializers import (
    Article,
    FavoriteArticleSerializer,
    FavoriteArticleListSerializer
)

LOOKUP_FIELD = 'slug'


class FavoriteArticleListAPIView(ListCreateAPIView):
    """ List user favourited articles """
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = FavoriteArticleListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Article.objects.filter(favorites__id=self.request.user.id)

        return queryset_list


class FavoriteArticleUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """ Favorites an article """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Article.objects.all()
    lookup_field = LOOKUP_FIELD
    serializer_class = FavoriteArticleSerializer

    def perform_destroy(self, instance):
        instance.favorites.remove(self.request.user)
