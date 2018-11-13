from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.timezone import now
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


    class Meta:
        app_label = 'comment'

