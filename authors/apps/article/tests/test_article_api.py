from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import ArticleFactory, UserFactory

faker = Factory.create()


class ArticleApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = ArticleFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'article_api'
        self.body = {
            'title': faker.name(),
            'description': faker.text(),
            'body': faker.text(),
            'tags': ["tags","test"]
        }
        self.create_url = reverse(self.namespace + ':create')
        self.list_url = reverse(self.namespace + ':list')
        self.update_url = reverse(
            self.namespace + ':update', kwargs={'slug': self.article.slug})
        self.delete_url = reverse(
            self.namespace + ':delete', kwargs={'slug': self.article.slug})
        self.retrieve_url = reverse(
            self.namespace + ':detail', kwargs={'slug': self.article.slug})
        self.like_url = reverse(self.namespace + ':like',
                                kwargs={'slug': self.article.slug})
        self.dislike_url = reverse(self.namespace + ':dislike',
                                   kwargs={'slug': self.article.slug})
        self.dislikers_url = reverse(
            self.namespace + ':dislikers', kwargs={'slug': self.article.slug})
        self.likers_url = reverse(
            self.namespace + ':likers', kwargs={'slug': self.article.slug})

    def test_create_article_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.assertEqual(201, response.status_code)

    def test_retrieve_article_api(self):
        response = self.client.get(self.retrieve_url)
        self.assertContains(response, self.article)

    def test_list_article_api_with_parameters(self):
        self.client.post(self.create_url, self.body, format='json')
        response = self.client.get(
            self.list_url + '?q=' + self.article.slug[0])
        self.assertContains(response, self.article)

    def test_list_article_custom_filters(self):
        self.client.post(self.create_url, self.body, format='json')
        response = self.client.get(
            self.list_url + '?tag=' + self.body['tags'][0])
        response2 = self.client.get(
            self.list_url + '?author=' + self.user.username)
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response2.status_code)

    def test_listing_articles_api(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, self.article)

    def test_update_article_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.update_url = reverse(
            self.namespace + ':update', kwargs={'slug': response.data.get('slug')})
        response = self.client.put(self.update_url, self.body)
        self.assertEqual(200, response.status_code)

    def test_delete_article_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.delete_url = reverse(
            self.namespace + ':delete', kwargs={'slug': response.data.get('slug')})
        response = self.client.delete(self.delete_url)
        self.assertEqual(204, response.status_code)

    def test_like_article(self):
        res = self.client.post(self.like_url)
        self.assertEqual(200, res.status_code)

    def test_dislike_article(self):
        res = self.client.post(self.dislike_url)
        self.assertEqual(200, res.status_code)

    def test_cancel_like(self):
        self.client.post(self.like_url)
        res = self.client.post(self.like_url)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "Like cancelled successfully.")

    def test_cancel_dislike(self):
        self.client.post(self.dislike_url)
        res = self.client.post(self.dislike_url)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "Dislike cancelled successfully.")

    def test_get_likers(self):
        res = self.client.get(self.likers_url)
        self.assertEqual(200, res.status_code)

    def test_get_dislikers(self):
        res = self.client.get(self.dislikers_url)
        self.assertEqual(200, res.status_code)

    def test_reading_time_of_article(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.json().get('reading_time'), '1 min read')
    
    def test_social_media_sharing_links(self):
        response = self.client.get(self.retrieve_url)
        self.assertIn('http://www.facebook.com/sharer.php?u=', response.json().get('facebook'))
        self.assertIn('https://twitter.com/share?url=', response.json().get('twitter'))
        self.assertIn('http://www.linkedin.com/shareArticle?url=', response.json().get('Linkedin'))
        self.assertIn('http://www.linkedin.com/shareArticle?url=', response.json().get('Linkedin'))
        self.assertIn('mailto:?subject=Checkout this great read', response.json().get('mail'))




        
