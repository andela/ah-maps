"""Define different notification functionality."""

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from authors.apps.notifications.models import Notification
from .serializers import NotificationSerializer, TABLE


def send_email_notification(recepient, message, request):
    """Send an email notification to subscribed users."""
    if not recepient.subscribed:
        return
    protocol = 'https://' if request.is_secure() else 'http://'
    current_site = get_current_site(request)
    unsubscribe_url = protocol + current_site.domain + \
        reverse('notifications_api:subscription')
    profile_url = protocol + current_site.domain + \
        reverse('profile_api:detail', kwargs={
                "user__username": request.user.username})
    message = "<a href='" + profile_url + "'>" + message + "</a>"
    message = message + "<br><br>Click <a href='" + unsubscribe_url + \
        "'>this link</a> link to unsubscribe from email notifications"
    send_mail("Authors' Haven Notification", message, settings.COMPANY_EMAIL, [
              recepient.user.email], fail_silently=True,  html_message=message)


def notify_liked_article(article, liked_by, request):
    """Notify author of a liked article."""
    message = "Your article '{}' has been liked by {}.".format(
        article.title, liked_by.user.username)
    note = Notification(article=article, user=article.user.profile,
                        associating_user=liked_by, message=message)
    note.save()
    send_email_notification(recepient=article.user.profile,
                            message=message, request=request)


def notify_followed_by(follower, followed, request):
    """Notification for new follower."""
    message = 'You have been followed by {}.'.format(follower.user.username)
    note = Notification(
        user=followed, associating_user=follower, message=message)
    note.save()
    send_email_notification(recepient=followed,
                            message=message, request=request)


def notify_article_commented(article, comment_by, request):
    """Notify author of new comments on their articles."""
    message = "Your article '{}' has a new comment by {}.".format(
        article.title, comment_by.user.username)
    note = Notification(user=article.user.profile,
                        associating_user=comment_by, article=article, message=message)
    note.save()
    send_email_notification(recepient=article.user.profile,
                            message=message, request=request)


def notify_activity_on_favorited_article(article, comment_by, favorited_by, request):
    """Notify user of any activity on a favorited article."""
    message = "The '{}' article has a new comment by {}.".format(
        article.title, comment_by.user.username)
    note = Notification(user=favorited_by, article=article,
                        associating_user=favorited_by, message=message)
    note.save()
    send_email_notification(recepient=favorited_by,
                            message=message, request=request)

def notify_followed_user_posts_article(follower, article, request):
    """Notify user when a profile they are following posts a new article."""
    message = "{} has posted a new article '{}'.".format(
        article.user.username, article.title)
    note = Notification(user=follower, associating_user=article.user.profile,
                        article=article, message=message)
    note.save()
    send_email_notification(recepient=follower,
                            message=message, request=request)


class NotificationsListAPIView(RetrieveUpdateDestroyAPIView):
    """Get and destroy a users notifications."""

    permission_classes = [IsAuthenticated, ]
    serializer_class = NotificationSerializer

    def get(self, request, id=None):
        """Get one notification or all of them."""
        if id:
            # Show that specific notification
            try:
                instance = TABLE.objects.get(pk=id, user=request.user.profile)
                instance.seen_read = True
                instance.save()
                instance = TABLE.objects.filter(
                    pk=id, user=request.user.profile)
                res = instance.values('id', 'associating_user__user__username',
                                      'user__user__username', 'message', 'article__slug', 'seen_read')
                return Response(list(res), status=status.HTTP_200_OK)

            except TABLE.DoesNotExist:
                raise serializers.ValidationError(
                    "The current user has no Notification with the provided id.")

        # If there is no id display all notifications
        instance = TABLE.objects.filter(user=request.user.profile)
        res = instance.values('id', 'associating_user__user__username',
                              'user__user__username',
                              'message', 'article__slug', 'seen_read')
        return Response(list(res), status=status.HTTP_200_OK)

    def delete(self, request, id):
        """Delete a notification."""
        try:
            instance = TABLE.objects.get(pk=id, user=request.user.profile)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TABLE.DoesNotExist:
            raise serializers.ValidationError(
                "The provided id has no matching notification for this user.")


class NotificationsSubscriptionAPIView(RetrieveUpdateDestroyAPIView):
    """Subscribe and unsubscribe a user from email notifications."""

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        """Subscribe to email notifications."""
        if request.user.profile.subscribed:
            request.user.profile.subscribed = False
            request.user.profile.save()
            message = {
                "message": "You have been successfully unsubscribed from email notifications."}
            return Response(message, status=status.HTTP_200_OK)

        request.user.profile.subscribed = True
        request.user.profile.save()
        message = {
            "message": "You have been successfully subscribed to email notifications."}
        return Response(message, status=status.HTTP_200_OK)
