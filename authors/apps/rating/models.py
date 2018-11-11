from django.db import models
from django.contrib.auth import get_user_model

from django.apps import apps
from ..article.models import Article

class Rating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='rater',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        related_name='rated_article',
        on_delete=models.CASCADE
    )

    your_rating = models.FloatField(null=False)
    
    class Meta:
        app_label = 'rating'

    def __str__(self):
        return self.article.title

    def average_rating(self):
        average = self.aggregate(models.Avg('your_rating'))
        return average['your_rating__avg']

