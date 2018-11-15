"""Bookmark views."""
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework import serializers, status
from authors.apps.article.api.serializers import TABLE
from .serializers import BookMarkSerializer
from authors.apps.article.api.views import get_article



class BookMarkListAPIView(ListAPIView):
    """List current users bookmarks."""

    permission_classes = (IsAuthenticated,)
    serializer_class = BookMarkSerializer

    def get(self, request):
        """Get my bookmarks."""
        bookmarks = request.user.profile.my_bookmarks.all().values('slug', 'title', 'image', 'user__username')
        message = {"MyBookmarks": bookmarks}
        return Response(message, status=status.HTTP_200_OK)


class BookMarkArticleAPIView(RetrieveUpdateDestroyAPIView):
    """Create and Destroy Bookamrks."""

    permission_classes = (IsAuthenticated,)
    serializer_class = BookMarkSerializer

    def post(self, request, slug):
        """Create a bookmark."""
        article = get_article(slug)

        # Check if the article has been bookmarked before
        bookmarked = request.user.profile.my_bookmarks.filter(slug=slug)
        if bookmarked:
            raise serializers.ValidationError(
                "You cannot bookmark an article twice.")
        # If it has not been bookmarked before, bookmark it

        article.bookmark_article(request.user.profile)

        message = {
            "success": "Article {} bookmarked successfully".format(article.title)}
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """Unbookmark an article."""
        article = get_article(slug)

        # Check if the article had been bookmarked
        bookmarked = request.user.profile.my_bookmarks.filter(slug=slug)
        if not bookmarked:
            raise serializers.ValidationError(
                "You cannot unbookmark an article you haven't bookmarked.")
        # If it was bookmarked, unbookmark it

        article.unbookmark_article(request.user.profile)

        message = {
            "success": "Article {} unbookmarked successfully".format(slug)}
        return Response(message, status=status.HTTP_200_OK)
