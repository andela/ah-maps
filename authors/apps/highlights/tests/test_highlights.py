"""Highlights api tests."""

import random
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import ArticleFactory, UserFactory

faker = Factory.create()


class HighlightsApiTest(TestCase):
    """Test the highlights."""

    def setUp(self):
        """Initialize tests."""
        self.user = UserFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)
        self.namespace = 'highlights_api'
        self.highlight_url = reverse(
            self.namespace + ':create_highlight', kwargs={'slug': self.article.slug})
        self.highlight = random.choices(self.article.body.split(' '))
        self.data = {"comment": "This is a comment.",
                     "highlight": self.highlight}
        self.fake_data = {"comment": "This is a comment.",
                          "highlight": "Text not in article body."}
        self.highlight_fake_article_url = reverse(
            self.namespace + ':create_highlight', kwargs={'slug': 'not-real-slug'})

    def test_create_highlight(self):
        """Test creating a highlight."""
        res = self.client.post(self.highlight_url, data=self.data)
        self.assertEqual(201, res.status_code)

    def test_update_highlight(self):
        """Test update a highlight functionality."""
        self.client.post(self.highlight_url, data=self.data)
        res = self.client.post(self.highlight_url, data=self.data)
        self.assertContains(res, 'updated')

    def test_highlight_text_not_in_article(self):
        """Test highlight non-existing text."""
        res = self.client.post(self.highlight_url, data=self.fake_data)
        self.assertEqual(404, res.status_code)

    def test_get_my_highlights(self):
        """Test get my highlights functionality."""
        self.list_url = reverse('article_api' + ':list')
        res = self.client.get(self.list_url)
        self.assertContains(res, 'my_highlights')

    def test_delete_highlight(self):
        """Test delete highlight functionality."""
        res = self.client.post(self.highlight_url, data=self.data)
        self.delete_highlight = reverse(self.namespace + ':remove_highlight', kwargs={
            'article_slug': self.article.slug, 'highlight_slug': res.data.get('success')[0].get('slug')})
        res = self.client.delete(self.delete_highlight)
        self.assertEqual(204, res.status_code)

    def test_delete_non_existing(self):
        """Test delete non existent highlight."""
        self.delete_highlight = reverse(self.namespace + ':remove_highlight', kwargs={
            'article_slug': self.article.slug, 'highlight_slug': "random text not highlighted"})
        res = self.client.delete(self.delete_highlight)
        self.assertEqual(404, res.status_code)

    def test_highlight_non_existing_article(self):
        """Test highlight non existing article."""
        res = self.client.post(self.highlight_fake_article_url, data=self.data)
        self.assertEqual(400, res.status_code)
