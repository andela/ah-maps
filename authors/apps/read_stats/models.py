"""Define the readers model."""

from django.db import models
from authors.apps.profile.models import Profile
from authors.apps.article.models import Article


class Readers(models.Model):
    """The reader model."""

    reader = models.ForeignKey(
        Profile,
        related_name='read_by',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        """define metadata."""

        app_label = 'read_stats'

    def __str__(self):
        """Print out as title."""
        return self.article.title
