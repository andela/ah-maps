from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView
)

from rest_framework.permissions import (
    IsAuthenticated,
)
from .serializers import (
    Comment,
    LikeCommentSerializer,
    DisLikeCommentSerializer
)


class LikeCommentUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """ Like an comment """
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = LikeCommentSerializer
    lookup_field = 'pk'


class DisLikeCommentUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """ DisLike an comment """
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = DisLikeCommentSerializer
