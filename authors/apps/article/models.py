"""Define the article model."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField

from ..tags.models import Tag
from authors.apps.profile.models import Profile

from rest_framework.reverse import reverse as api_reverse



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
    slug = AutoSlugField(populate_from='title', blank=True, null=True, unique=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='tagged_articles',
    )
    title = models.CharField(
        _('Article field', 'title'),
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
    favorites = models.ManyToManyField(
        get_user_model(),
        related_name='user_favorites',
        null=True,
        blank=True
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
    bookmarked_by = models.ManyToManyField(
        Profile, related_name='my_bookmarks', symmetrical=True)

    def bookmark_article(self, profile):
        """Create a bookmark for a specific user."""
        profile.my_bookmarks.add(self)

    def unbookmark_article(self, profile):
        """Destroy a bookmark."""
        profile.my_bookmarks.remove(self)

    def like_article(self, profile):
        """Like an article."""
        profile.liked_articles.add(self)

    def dislike_article(self, profile):
        """Dislike an article."""
        profile.disliked_articles.add(self)

    def get_likers(self):
        """Get profiles that like the article."""
        return self.liked_by.all()

    def get_dislikers(self):
        """Get profiles that dislike this article."""
        return self.disliked_by.all()

    def unlike_article(self, profile):
        """Unlike an article."""
        profile.liked_articles.remove(self)

    def undislike_article(self, profile):
        """Undislike an article."""
        profile.disliked_articles.remove(self)

    class Meta:
        """define metadata."""

        app_label = 'article'

    def __str__(self):
        """Print out as title."""
        return self.title

    def article_url(self,request=None):
        return api_reverse("article_api:detail",kwargs={'slug':self.slug},request=request)

    def is_favorited(self, user=None):
        """Get favourited articles."""
        queryset = self.favorites.all()
        queryset = queryset.filter(id=user.id) if user else queryset
        return queryset.count()
