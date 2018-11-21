"""Notification serializers."""

from rest_framework import serializers
from django.apps import apps

TABLE = apps.get_model('notifications', 'Notification')


class NotificationSerializer(serializers.ModelSerializer):
    """Serialize notification data."""

    class Meta:
        """Serializer metadata."""

        model = TABLE

        fields = ('pk', 'associating_user', 'user', 'message', 'article', 'seen_read')
