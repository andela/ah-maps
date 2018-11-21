"""Test the notifications functionality."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import ArticleFactory
from authors.apps.factories.profile import ProfileFactory

faker = Factory.create()


class NotificationsApiTest(TestCase):
    """Bookmark tests."""

    def setUp(self):
        """Set up bookmark tests."""
        self.profile = ProfileFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.article.user.token)
        self.namespace = 'notifications_api'
        self.notifications_url = reverse(self.namespace + ':get_all')
        self.unsubscribe_url = reverse(self.namespace + ':subscription')
        self.like_url = reverse('article_api' + ':like',
                                kwargs={'slug': self.article.slug})
        self.fake_notification_url = reverse(
            self.namespace + ':get_one', kwargs={"id": 10})

    def test_get_all_notifications(self):
        """Test user can get all notifications."""
        self.client.post(self.like_url)
        res = self.client.get(self.notifications_url)
        self.assertEqual(200, res.status_code)

    def test_get_one_notification(self):
        """Test get one notification."""
        self.client.post(self.like_url)
        res = self.client.get(self.notifications_url)
        self.notification_url = reverse(
            self.namespace + ':get_one', kwargs={"id": res.data[0].get('id')})
        res = self.client.get(self.notification_url)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, 'has been liked by')

    def test_delete_notification(self):
        """Test delete a notification."""
        self.client.post(self.like_url)
        res = self.client.get(self.notifications_url)
        self.notification_url = reverse(
            self.namespace + ':get_one', kwargs={"id": res.data[0].get('id')})
        res = self.client.get(self.notification_url)
        res = self.client.delete(self.notification_url)
        self.assertEqual(204, res.status_code)

    def test_delete_non_existing_notification(self):
        """Test delete fake notification."""
        res = self.client.delete(self.fake_notification_url)
        self.assertEqual(400, res.status_code)

    def test_unsubscribe_to_email_notifications(self):
        """Test unsubscribe from email notification."""
        res = self.client.get(self.unsubscribe_url)
        self.assertEqual(200, res.status_code)
        self.assertContains(
            res, "You have been successfully unsubscribed from email notifications.")

    def test_subscribe_to_email_notification(self):
        """Test subscribe to email notifications."""
        self.client.get(self.unsubscribe_url)
        res = self.client.get(self.unsubscribe_url)
        self.assertContains(
            res, "You have been successfully subscribed to email notifications.")
        self.assertEqual(200, res.status_code)
