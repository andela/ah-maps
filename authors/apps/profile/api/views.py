from rest_framework.generics import (
  ListAPIView,
  RetrieveUpdateAPIView,
  RetrieveAPIView,
)
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly
)
from .serializers import (
    TABLE, ProfileListSerializer, ProfileUpdateSerializer
)
from ...core.permissions import IsOwnerOrReadOnly


class ProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProfileListSerializer
    queryset = TABLE.objects.all()


class ProfileDetailAPIView(RetrieveAPIView):
    queryset = TABLE.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'user__username'


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TABLE.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'user__username'
