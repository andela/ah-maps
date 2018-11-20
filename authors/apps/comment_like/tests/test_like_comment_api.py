from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ...factories import (
    ArticleFactory,
    CommentFactory,
    UserFactory
)


class LikeCommentAPITest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.comment = CommentFactory()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

        self.namespace = 'comment_like_api'
        self.like_url = reverse(self.namespace + ':like', kwargs={'pk': self.comment.pk})
        self.dislike_url = reverse(self.namespace + ':dislike', kwargs={'pk': self.comment.pk})

    def test_like_comment(self):
        response = self.client.put(self.like_url)
        self.assertEqual(200, response.status_code)

        response = self.client.put(self.like_url)
        self.assertEqual(200, response.status_code)

    def test_dislike_comment(self):
        response = self.client.put(self.dislike_url)
        self.assertEqual(200, response.status_code)

        response = self.client.put(self.dislike_url)
        self.assertEqual(200, response.status_code)
