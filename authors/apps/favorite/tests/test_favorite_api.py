from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ...factories import ArticleFactory, UserFactory


class FavoriteAPITest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'favorite_api'
        self.favorite_url = reverse(self.namespace + ':update', kwargs={'slug': self.article.slug})
        self.favorites_url = reverse(self.namespace + ':list')

    def test_favorite_article(self):
        response = self.client.put(self.favorite_url)
        self.client.get(self.favorites_url)
        self.assertEqual(200, response.status_code)

    def test_unfavorite_article(self):
        response = self.client.delete(self.favorite_url)
        self.assertEqual(204, response.status_code)

    def test_list_favorite_articles(self):
        response = self.client.get(self.favorites_url)
        self.assertEqual(200, response.status_code)

