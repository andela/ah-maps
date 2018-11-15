from django.apps import apps
from rest_framework import status
from rest_framework.generics import (
  ListAPIView,
  ListCreateAPIView,
  DestroyAPIView
)
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from .serializers import TagSerializer, TagsSerializer, TagCreateSerializer
from ...core.permissions import IsOwnerOrReadOnly

LOOKUP_FIELD = 'slug'
TAG = apps.get_model('tags', 'Tag')
TABLE = apps.get_model('article', 'Article')


class ArticleTagsAPIView(ListCreateAPIView, DestroyAPIView):
    lookup_field = LOOKUP_FIELD
    serializer_class = TagSerializer
    queryset = TAG.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """ Function to create a tag for an article
        """
        slug = kwargs['slug']

        article =TABLE.objects.filter(
            slug=slug, user=request.user).first() #fetch article by slug

        if article is None:
            return Response({
                'errors': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)

        else:
            requested = TagCreateSerializer(data=request.data)
            requested.is_valid(raise_exception=True)

            tags = requested.data.get('tags', []) #tags should be provided as a list

            serializer = self.serializer_class(
                many=True, data=[{
                    'tag': x
                } for x in tags])


            valid = serializer.is_valid(raise_exception=False)

            if not valid:
                errors = {}
                for i in range(0, len(serializer.errors)):
                    if len(serializer.errors[i]) > 0:
                        errors[tags[i]] = serializer.errors[i]['tag']
                return Response(errors, status.HTTP_400_BAD_REQUEST)

            for tag in tags:
                t, created = TAG.objects.get_or_create(tag=tag)
                article.tags.add(t)

            response = TagsSerializer(article)
            return Response(response.data)

    def destroy(self, request, *args, **kwargs):
        slug = kwargs['slug']

        article =TABLE.objects.filter(
            slug=slug, user=request.user).first()

        if article is None:
            return Response({
                'errors': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)

        else:
            requested = TagCreateSerializer(data=request.data)
            requested.is_valid(raise_exception=True)

            tags = requested.data.get('tags', []) #tags should be provided as a list

            # delete the tags from the article specified
            for tag in tags:
                deleted_tag = TAG.objects.get(tag=tag) #fetch the tag
                if deleted_tag:
                    article.tags.remove(deleted_tag) #remove the tag from the article

            response = TagsSerializer(article)
            return Response(response.data)

    def list(self, request, *args, **kwargs):
        """
            View all the tags of a particular article
        """

        slug = kwargs['slug']

        article = TABLE.objects.filter(
            slug=slug, user=request.user).first()

        if article is None:
            return Response({
                'errors': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)
        else:

            response = TagsSerializer(article)
            return Response(response.data)


class TagsView(ListCreateAPIView):
    queryset = TAG.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
