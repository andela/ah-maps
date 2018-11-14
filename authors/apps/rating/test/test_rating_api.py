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

        self.rating_body = {
            'your_rating' : 5
        }

        self.create_url = reverse('article_api:create')

        # post an article for rating tests
        self.post_article = self.client.post(self.create_url, self.body, format='json')


    def test_post_rating(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})

        #when logged in
        response = self.client2.post(self.rate_article_url, self.rating_body, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json().get('average_rating'), self.article_rating)
        self.assertEqual(response.json().get('your_rating'), self.article_rating)

        #when not logged in
        response = self.client3.post(self.rate_article_url, self.rating_body, format='json')

        self.assertEqual(401, response.status_code)
        self.assertEqual(response.json().get('detail'), 'Authentication credentials were not provided.')

    def test_get_rating(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})
        self.client2.post(self.rate_article_url, self.rating_body, format='json')
        # when logged in
        get_rating = self.client2.get(self.rate_article_url)

        self.assertEqual(200, get_rating.status_code)
        self.assertEqual(get_rating.json().get('average_rating'), self.article_rating)
        self.assertEqual(get_rating.json().get('your_rating'), self.article_rating)

        # when not logged in
        get_rating2 = self.client3.get(self.rate_article_url)

        self.assertEqual(200, get_rating2.status_code)
        self.assertEqual(get_rating2.json().get('article'), self.article_slug)
        self.assertEqual(get_rating2.json().get('average_rating'), self.article_rating)
        self.assertEqual(get_rating2.json().get('your_rating'), "Sorry, you can't see your rating because you are not logged in")

        # when logged in but haven't rated the article
        self.client2.delete(self.rate_article_url, self.rating_body, format='json')
        get_rating = self.client2.get(self.rate_article_url)

        self.assertEqual(200, get_rating.status_code)
        self.assertEqual(get_rating.json().get('article'), self.article_slug)
        self.assertEqual(get_rating.json().get('your_rating'), 'Sorry, you have not rated this article')

    def test_cannot_rate_own_article(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})
        response = self.client.post(self.rate_article_url, self.rating_body, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json().get('errors').get('author'), 'Sorry, you cannot rate your own article')

    def test_cannot_rate_missing_article(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': 'this-slug-is-fake'})
        response = self.client2.post(self.rate_article_url, self.rating_body, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json().get('errors').get('article'), 'Sorry, none of our articles has that slug')

    def test_user_can_delete_rating(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})
        self.client2.post(self.rate_article_url, self.rating_body, format='json')

        # delete existing rating
        first_delete_request = self.client2.delete(self.rate_article_url)
        self.assertEqual(200, first_delete_request.status_code)
        self.assertEqual(first_delete_request.json().get('message'), 'Successfully deleted rating')

        # delete non-existing rating
        second_delete_request = self.client2.delete(self.rate_article_url)
        self.assertEqual(404, second_delete_request.status_code)
        self.assertEqual(second_delete_request.json().get('rating'), 'Sorry, you have not rated this article')

    def test_user_must_rate_between_1_and_5(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})
        response1 = self.client2.post(self.rate_article_url, {"your_rating" : 6}, format='json')
        response2 = self.client2.post(self.rate_article_url, {"your_rating" : -1}, format='json')

        self.assertEqual(400, response1.status_code)
        self.assertEqual(400, response2.status_code)
        
    def test_posting_again_updates_previous_value(self):
        self.rate_article_url = reverse('rating_api:rate', kwargs={'slug': self.post_article.data.get('slug')})
        self.client2.post(self.rate_article_url, { "your_rating" : 1 }, format='json')
        response2 = self.client2.post(self.rate_article_url, { "your_rating" : 2 }, format='json')

        self.assertEqual(201, response2.status_code)
        self.assertEqual(response2.json().get('your_rating'), 2.0)
