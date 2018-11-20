from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from authors.apps.article.models import Article


class Comment(models.Model):
    """ Represent model for a comment. """
    user = models.ForeignKey(
        get_user_model(),
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    # Bound comment to article class
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    body = models.TextField(
        _('Comment Field', 'body'),
        blank=True,
        null=True
    )
    # Create a recursive relationship so that comment has many-to-one relationship
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='thread'
    )
    created_at = models.DateTimeField(
        _('Comment field', 'created at'),
        auto_now_add=True,
        editable=False

    )
    updated_at = models.DateTimeField(
        _('Comment field', 'updated at'),
        auto_now=True
    )
    likes = models.ManyToManyField(
        get_user_model(),
        related_name='comment_likes')
    dislikes = models.ManyToManyField(
        get_user_model(),
        related_name='comment_dislikes')

    class Meta:
        app_label = 'comment'

    def __str__(self):
        return self.body

    def get_likes(self, user=None):
        """Get number of comment likes."""
        queryset = self.likes.all()
        queryset = queryset.filter(id=user.id) if user else queryset
        return queryset.count()

    def get_dislikes(self, user=None):
        """Get number of comment dislikes."""
        queryset = self.dislikes.all()
        queryset = queryset.filter(id=user.id) if user else queryset
        return queryset.count()
