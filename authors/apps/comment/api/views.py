from django.db.models import Q
from rest_framework.generics import (
  ListAPIView, CreateAPIView,
  RetrieveUpdateAPIView,
  RetrieveAPIView,
  DestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly
)
from .serializers import TABLE, CommentSerializer, CommentCreateSerializer, Article
from ...core.permissions import IsOwnerOrReadOnly

LOOKUP_FIELD = 'pk'


class CommentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentCreateSerializer
    lookup_field = 'slug'

    def get_queryset(self, *args, **kwargs):
        """get all comment"""
        queryset_list = TABLE.objects.all()

        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(body__icontains=query) 
            )

        return queryset_list.order_by('-id')


class CommentCreateAPIView(RetrieveUpdateAPIView, CreateAPIView):
    """ create a comment."""
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = TABLE.objects.all()
    lookup_field = 'slug'

    def post(self, request, slug):
        """create a comment."""
        article = Article.objects.get(slug=slug)
        serializer = CommentCreateSerializer(data={"article":article,"body":request.data.get('body')})
        if serializer.is_valid():
            data = serializer.save(body=request.data.get('body'), user=self.request.user, article=article)
            username = data.get('user').username
            slug = article.slug
            comment_id = TABLE.objects.last().id
            data = {"article": slug, "author": username, "comment": request.data.get('body'), "id" : comment_id}
            message = {"comment": data}
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'invalid data'}, status=status.HTTP_200_OK)



class CommentDetailAPIView(RetrieveAPIView):
    """check for comment details."""
    queryset = TABLE.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'

class CommentDeleteAPIView(DestroyAPIView):
    """delete a comment."""
    queryset = TABLE.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer


class CommentUpdateAPIView(RetrieveUpdateAPIView, CreateAPIView):
    """edit a comment."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = TABLE.objects.all()
    serializer_class = CommentCreateSerializer
    lookup_field = LOOKUP_FIELD

    def perform_update(self, serializer):
        """edit a comment."""
        serializer.save(user=self.request.user)

    def create(self, request, pk=None, **kwargs):
        """
        Handles the creation of replies
        """
        data = request.data
        context = {'request': request}
        queryset = TABLE.objects.all()
        context['parent'] = TABLE.objects.get(pk=pk)
        if context['parent']:
            serializer = self.serializer_class(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"Message": "Comment requested was not found"})
