from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField


class Article(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='author',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    slug = AutoSlugField(populate_from='title', blank=True, null=True, unique=True)
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

    class Meta:
        app_label = 'article'

    def __str__(self):
        return self.title

    def is_favorited(self, user=None):
        queryset = self.favorites.all()
        queryset = queryset.filter(id=user.id) if user else queryset
        return queryset.count()
