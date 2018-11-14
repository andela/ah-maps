from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth import get_user_model

from django.apps import apps
from ..article.models import Article

class Report(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='reporter',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article,
        related_name='reports',
        on_delete=models.CASCADE
    )
    
    message = models.TextField(
        _('Report Field', 'message'),
        blank=True,
        null=True
    )

    category = models.TextField(
        _('Report Field', 'category'),
        blank=True,
        null=True
    )
    
    class Meta:
        app_label = 'report'

    def __str__(self):
        return self.message
