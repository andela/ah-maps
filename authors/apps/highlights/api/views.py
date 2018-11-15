"""Highlights api views."""

from datetime import datetime as dt
from datetime import timezone

from rest_framework.generics import (
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from django.apps import apps
from rest_framework.response import Response
from rest_framework import status, serializers
import readtime
from authors.apps.article.api.views import get_article
from .serializers import HighlightsSerializer, TABLE


class AddHighlightAPIView(RetrieveUpdateAPIView):
    """Highlight text in some article."""

    permission_classes = (IsAuthenticated,)
    serializer_class = HighlightsSerializer

    def post(self, request, slug):
        """Post a highlight for an article."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = request.user.profile
        highlight = serializer.validated_data.get('highlight')
        comment = serializer.validated_data.get('comment')
        article = get_article(slug)

        # Check if highlighted text is in article body
        if highlight in article.body:
            # Check if highlight has been made before
            try:
                exists = TABLE.objects.get(
                    article=article, highlight=highlight, author=author)
                # If it exists update
                exists.comment = comment
                exists.save()
                ret = TABLE.objects.filter(
                    article=article, highlight=highlight, author=author)
                message = {"updated": ret.values(
                    'slug', 'article__slug', 'comment')}
                return Response(message, status=status.HTTP_200_OK)

            except TABLE.DoesNotExist:
                # Save the highlight
                instance = TABLE(article=article, author=author,
                                 highlight=highlight, comment=comment)
                instance.save()

                message = {"success": TABLE.objects.filter(article=article, author=author,
                                                           highlight=highlight, comment=comment).values(
                    'slug', 'article__slug', 'comment')}
                return Response(message, status=status.HTTP_201_CREATED)

        # If it's not in the article, fail
        else:
            message = {"error": "The highlight '{}' was not found in article '{}'.".format(highlight, article.title)}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, article_slug, highlight_slug):
        """Delete your highlights."""
        author = request.user.profile
        article = get_article(article_slug)
        # Check if highlight exists

        try:
            highlight = TABLE.objects.get(slug=highlight_slug, article=article, author=author)
            # If it exists delete it
            highlight.delete()
            message = {"Deleted": "Highlight deleted successfully."}
            return Response(message, status=status.HTTP_204_NO_CONTENT)

        except TABLE.DoesNotExist:
            message = {"error": "Highlight Not Found."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
