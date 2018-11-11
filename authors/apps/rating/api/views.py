from rest_framework import status
from rest_framework.generics import (
  GenericAPIView
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import (
 IsAuthenticatedOrReadOnly,
 IsAuthenticated
)

from rest_framework.exceptions import NotFound, ValidationError

from django.db.models import Avg

from django.apps import apps
from rest_framework.response import Response

from ...core.permissions import IsOwnerOrReadOnly
from django.contrib.sites.shortcuts import get_current_site

from .serializers import TABLE, RatingSerializer

Article = apps.get_model('article', 'Article')

def get_article(slug):
    """
    This returns articles based on the slug
    """
    article = Article.objects.filter(slug=slug).first()
    if not article:
        message = {'message': 'Sorry, we have no article with that slug'}
        return message
    return article


            
class RateAPIView(GenericAPIView):
    queryset = TABLE.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_rating(self, user, article):
        """
        Returns a rating given the user id and the article id
        """
        try:
            return TABLE.objects.get(user=user, article=article)
        except TABLE.DoesNotExist:
            raise NotFound(detail={'rating': 'Sorry, you have not rated this article'})

    def post(self, request, slug):
      rating = request.data
      article = get_article(slug)

      # ensures that article exists
      if isinstance(article, dict):
            raise ValidationError(detail={'article': 'Sorry, none of our articles has that slug'})

      # ensures a user cannot rate his/her own article
      if article.user == request.user:
            raise ValidationError(detail={'author': 'Sorry, you cannot rate your own article'})

      # updates a user's rating if it already exists
      try:
            # checks if rating exists....
            current_rating = TABLE.objects.get(
                user=request.user.id, 
                article=article.id
            )
            serializer = self.serializer_class(current_rating, data=rating)
      except TABLE.DoesNotExist:
            #  ....if it doesn't exist, a new one is created
            serializer = self.serializer_class(data=rating)

      serializer.is_valid(raise_exception=True)
      serializer.save(user=request.user, article=article)

      return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        rating = request.data
        article = get_article(slug)

        if isinstance(article, dict):
            raise ValidationError(detail={'article': 'Sorry, none of our articles has that slug'})
        # If the user is authenticated, return their rating as well but if not authenticated...
        # return only the average of the rating
        rating = None
        if request.user.is_authenticated:
            try:
                rating = TABLE.objects.get(user=request.user, article=article)
            except TABLE.DoesNotExist:
                pass

        if rating is None:
            avg = TABLE.objects.filter(article=article).aggregate(Avg('your_rating'))

            if request.user.is_authenticated:
                return Response({
                    'article': article.slug,
                    'average_rating': avg['your_rating__avg'],
                    'your_rating' : "Sorry, you have not rated this article"
                })
            else:
                return Response({
                    'article': article.slug,
                    'average_rating': avg['your_rating__avg'],
                    'your_rating' : "Sorry, you can't see your rating because you are not logged in"
                })

        
        serializer = self.serializer_class(rating)
        return Response(serializer.data)

    def delete(self, request, slug):
        """
        Deletes a rating
        """
        article = get_article(slug) 

        if isinstance(article, dict):
            raise ValidationError(detail={'article': 'Sorry, none of our articles has that slug'})
        rating = self.get_rating(user=request.user, article=article)
        rating.delete()
        return Response(
            {'message': 'Successfully deleted rating'}, 
            status=status.HTTP_200_OK
        )
