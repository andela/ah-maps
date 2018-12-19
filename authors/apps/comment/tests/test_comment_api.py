from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import CommentFactory, ArticleFactory, UserFactory

faker = Factory.create()


class CommentApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = ArticleFactory()
        self.comment = CommentFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'comment_api'
        self.body = {
            'body': faker.text()
        }
        self.create_url = reverse(self.namespace + ':comment', kwargs={'slug': self.article.slug})
        self.list_url = reverse(self.namespace + ':list', kwargs={'slug': self.article.slug})
        self.update_url = reverse(self.namespace + ':update', kwargs={'pk': self.comment.id})
        self.delete_url = reverse(self.namespace + ':delete', kwargs={'pk': self.comment.id})
        self.retrieve_url = reverse(self.namespace + ':detail', kwargs={'pk': self.comment.id})

    def test_create_comment_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.assertEqual(200, response.status_code)

    def test_retrieve_comment_api(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(200, response.status_code)

    def test_list_comment_api_without_parameters(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)

    def test_list_comment_api_with_parameters(self):
        self.client.post(self.create_url, self.body, format='json')
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)

    def test_update_module_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.update_url = reverse(self.namespace + ':update', kwargs={'pk': response.data.get('comment').get('id')})

        response = self.client.put(self.update_url, self.body)
        self.assertEqual(200, response.status_code)

    def test_delete_comment_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.delete_url = reverse(self.namespace + ':delete', kwargs={'pk': response.data.get('comment').get('id')})

        response = self.client.delete(self.delete_url)
        self.assertEqual(204, response.status_code)

    def test_get_liked_values(self):
        """Test the boolean values returned on liking."""
        like = 'comment_like_api'
        self.client.put(reverse(like + ':like', kwargs={'pk': self.comment.pk}))
        response = self.client.get(self.update_url)
        self.assertContains(response, 'liked')
        self.assertContains(response, 'disliked')

    def test_get_disliked_values(self):
        """Test the boolean values returned on liking."""
        like = 'comment_like_api'
        self.client.put(reverse(like + ':dislike', kwargs={'pk': self.comment.pk}))
        response = self.client.get(self.update_url)
        self.assertContains(response, 'liked')

    def test_get_comments_anonyous_user(self):
        """Test get comments by anonymous user."""
        unauthorized_client = APIClient()
        response = unauthorized_client.get(self.list_url)
        self.assertEqual(200, response.status_code)
