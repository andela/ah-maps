"""Define the article model."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from authors.apps.profile.models import Profile


class Article(models.Model):
    """The article model."""

    user = models.ForeignKey(
        get_user_model(),
        related_name='author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    slug = AutoSlugField(populate_from='title',
                         blank=True, null=True, unique=True)
    title = models.CharField(
        _('Article field', 'title'),
        unique=True,
        max_length=128
    )
    description = models.TextField(
        _('Article Field', 'description'),
        blank=True,
        null=True
    )
    body = models.TextField(
        _('Article Field', 'body'),
        blank=True,
        null=True
    )
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(
        _('Article field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Article field', 'updated at'),
        auto_now=True
    )
    liked_by = models.ManyToManyField(
        Profile, related_name='liked_articles', symmetrical=True)
    disliked_by = models.ManyToManyField(
        Profile, related_name='disliked_articles', symmetrical=True)

    def like_article(self, profile):
        """Like an article."""
        self.liked_by.add(profile)

    def dislike_article(self, profile):
        """Dislike an article."""
        self.disliked_by.add(profile)

    def get_likers(self):
        """Get profiles that like the article."""
        return self.liked_by.all()

    def get_dislikers(self):
        """Get profiles that dislike this article."""
        return self.disliked_by.all()

    def unlike_article(self, profile):
        """Unlike an article."""
        self.liked_by.remove(profile)

    def undislike_article(self, profile):
        """Undislike an article."""
        self.disliked_by.remove(profile)

    class Meta:
        """define metadata."""

        app_label = 'article'

    def __str__(self):
        """Print out as title."""
        return self.title
