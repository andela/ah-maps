from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from authors.configurations import settings
from django.db.models import Avg

TABLE = apps.get_model('rating', 'Rating')

class RatingSerializer(serializers.ModelSerializer):
    your_rating = serializers.FloatField(
        required=True,
        validators=[
            MinValueValidator(
                settings.RATING_MIN,
                message='Rating cannot be less than ' + str(settings.RATING_MIN)
            ),
            MaxValueValidator(
                settings.RATING_MAX,
                message='Rating cannot be more than ' + str(settings.RATING_MAX)
            )
        ],
        error_messages={
            'required': 'The rating is required'
        }
    )
    average_rating = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        average = TABLE.objects.filter(article=obj.article.id).aggregate(Avg('your_rating'))
        return average['your_rating__avg']

    def get_article(self, obj):
        return obj.article.slug

    def get_rating(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj
        return None

    class Meta:
        model = TABLE
        fields = ('article', 'average_rating', 'your_rating')