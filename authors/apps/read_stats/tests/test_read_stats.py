"""Read stats api tests."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import ArticleFactory, UserFactory
from authors.apps.factories.profile import ProfileFactory

faker = Factory.create()


class ReadStatsApiTest(TestCase):
    """Read stats test class."""

    def setUp(self):
        """Set up read stats tests."""
        self.user = UserFactory()
        self.profile = ProfileFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)
        self.namespace = 'read_stats_api'
        self.read_url = reverse(self.namespace + ':read',
                                kwargs={'slug': self.article.slug})
        self.my_reads = reverse(self.namespace + ':my_reads')

    def test_read_article(self):
        """Test read an article."""
        res = self.client.get(self.read_url)
        self.assertEqual(200, res.status_code)

    def test_read_article_before_set_read_time(self):
        """Test read an article before read time ends."""
        self.client.get(self.read_url)
        res = self.client.get(self.read_url)
        self.assertEqual(400, res.status_code)

    def test_articles_have_read_count(self):
        """Test read count functionality."""
        self.list_url = reverse('article_api' + ':list')
        res = self.client.get(self.list_url)
        self.assertContains(res, 'read_count')
