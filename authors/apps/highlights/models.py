"""Define the highlights models."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from autoslug import AutoSlugField
from authors.apps.profile.models import Profile
from authors.apps.article.models import Article


class Highlights(models.Model):
    """Define the model attributes."""

    author = models.ForeignKey(
        Profile, related_name='my_highlights', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='highlight', unique=True)
    highlight = models.TextField(
        _('Highlights Field', 'highlight'), null=False)
    article = models.ForeignKey(
        Article, related_name='my_highlights', on_delete=models.CASCADE)
    comment = models.TextField(
        _('Highlights Field', 'comment'), null=True)

    class Meta:
        """define metadata."""

        app_label = 'highlights'

    def __str__(self):
        """Print out as highlight."""
        return self.highlight
