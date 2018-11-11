from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import ArticleFactory, UserFactory

faker = Factory.create()


class ModuleApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.user2 = UserFactory()
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user2.token)

        self.user3 = UserFactory()
        self.client3 = APIClient()

        self.article_slug = "how-to-train-a-dragon"
        self.article_rating = 5.0
        
        self.body = {
            'title': "How to train a dragon",
            'description': "This is how you train a dragon",
            'body': "A description of how to train a dragon",
        }

        self.report_body = {
            'report' : "This article is abusive"
        }

        self.create_url = reverse('article_api:create')

        # post an article for rating tests
        self.post_article = self.client.post(self.create_url, self.body, format='json')


    def test_post_report(self):
        self.report_article_url = reverse('report_api:report', kwargs={'slug': self.post_article.data.get('slug')})

        #when logged in
        response = self.client2.post(self.report_article_url, self.report_body, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json().get('success'), "Your report has been successfully received")

        #when not logged in
        response = self.client3.post(self.report_article_url, self.report_body, format='json')

        self.assertEqual(401, response.status_code)
        self.assertEqual(response.json().get('detail'), 'Authentication credentials were not provided.')


    def test_cannot_report_own_article(self):
        self.rate_article_url = reverse('report_api:report', kwargs={'slug': self.post_article.data.get('slug')})
        response = self.client.post(self.rate_article_url, self.report_body, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json().get('errors').get('author'), 'Sorry, you cannot report your own article')

    def test_cannot_report_missing_article(self):
        self.rate_article_url = reverse('report_api:report', kwargs={'slug': 'this-slug-is-fake'})
        response = self.client2.post(self.rate_article_url, self.report_body, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json().get('errors').get('article'), 'Sorry, none of our articles has that slug')
