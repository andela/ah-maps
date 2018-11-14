"""Bookmark API tests."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import ArticleFactory, UserFactory
from authors.apps.factories.profile import ProfileFactory

faker = Factory.create()


class BookmarksApiTest(TestCase):
    """Bookmark tests."""

    def setUp(self):
        """Set up bookmark tests."""
        self.user = UserFactory()
        self.profile = ProfileFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)
        self.namespace = 'bookmark_api'
        self.bookmark_url = reverse(
            self.namespace + ':add', kwargs={'slug': self.article.slug})
        self.unbookmark_url = reverse(
            self.namespace + ':remove', kwargs={'slug': self.article.slug})
        self.list_bookmarks_url = reverse(self.namespace + ':list')
        self.bookmark_non_existing_url = reverse(
            self.namespace + ':remove', kwargs={'slug': "fake-slug"})
        self.unbookmark_non_existing_url = reverse(
            self.namespace + ':remove', kwargs={'slug': "fake-slug"})

    def test_bookmark_article(self):
        """Test bookmark an article."""
        res = self.client.post(self.bookmark_url)
        self.assertEqual(200, res.status_code)

    def test_bookmark_article_twice(self):
        """Test bookmark same article twice."""
        self.client.post(self.bookmark_url)
        res = self.client.post(self.bookmark_url)
        self.assertEqual(400, res.status_code)

    def test_unbookmark_article(self):
        """Test undo bookmark."""
        res = self.client.post(self.unbookmark_url)
        self.assertEqual(200, res.status_code)

    def test_unbookmark_article_not_bookmarked(self):
        """Test unbookmark unbookmarked article."""
        self.client.post(self.unbookmark_url)
        res = self.client.post(self.unbookmark_url)
        self.assertEqual(400, res.status_code)

    def test_bookmark_non_existing_article(self):
        """Test bookmark non-existing article."""
        res = self.client.post(self.bookmark_non_existing_url)
        self.assertEqual(400, res.status_code)

    def test_unbookmark_non_existing_article(self):
        """Test bookmark non-existing article."""
        res = self.client.post(self.unbookmark_non_existing_url)
        self.assertEqual(400, res.status_code)

    def test_list_my_bookmarks(self):
        """Test get my bookmarks."""
        res = self.client.get(self.list_bookmarks_url)
        self.assertEqual(200, res.status_code)
