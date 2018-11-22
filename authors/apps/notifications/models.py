"""Define the notifications model."""

from django.db import models
from django.utils.translation import pgettext_lazy as _
from authors.apps.profile.models import Profile
from authors.apps.article.models import Article


class Notification(models.Model):
    """The notifications model."""

    user = models.ForeignKey(
        Profile, related_name='my_notifications', null=False, on_delete=models.CASCADE)
    message = models.CharField(
        _('Notification field', 'message'), max_length=128)
    seen_read = models.BooleanField(default=False)
    associating_user = models.ForeignKey(
        Profile, null=False, on_delete=models.CASCADE, related_name='my_activity')
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)


    class Meta:
        """define metadata."""

        app_label = 'notifications'

    def __str__(self):
        """Print out as message."""
        return self.message
