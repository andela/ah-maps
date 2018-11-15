from rest_framework import serializers
from django.apps import apps
from authors.apps.article.api.views import get_article

Article = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')
TABLE = apps.get_model('highlights', 'Highlights')

NAMESPACE = 'highlight_api'
fields = ('comment', 'highlight')


class HighlightsSerializer(serializers.ModelSerializer):
    """Highlight serializer."""

    highlight = serializers.CharField(required=True, error_messages={
        'required': 'Sorry, highlight is required.',
    })
    comment = serializers.CharField(required=True, error_messages={
        'required': 'Sorry, comment is required.',
    })

    class Meta:
        """Metadata description."""

        model = TABLE

        fields = fields
