from rest_framework import status
from rest_framework.generics import (
  ListAPIView,
  RetrieveUpdateAPIView,
  RetrieveAPIView,
)
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly,
 IsAuthenticated
)
from rest_framework.response import Response
from .serializers import (
    TABLE, ProfileListSerializer, ProfileUpdateSerializer
)
from ...core.permissions import IsOwnerOrReadOnly
from django.contrib.sites.shortcuts import get_current_site

class ProfileListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileListSerializer
    queryset = TABLE.objects.all()


class ProfileDetailAPIView(RetrieveAPIView):
    queryset = TABLE.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'user__username'

class MyProfileDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileListSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user.profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TABLE.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'user__username'
