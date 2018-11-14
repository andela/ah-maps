from django.test import TestCase
from django.apps import apps
from ...factories import CommentFactory

Comment = apps.get_model('comment', 'Comment')

class CommentModelTest(TestCase):
    def setUp(self):
        self.data = {
            'body': 'this is the body section',
        }

    def test_model_can_create_comment(self):
        comment = CommentFactory(body=self.data.get('body'))
        saved_comment = Comment.objects.get(body=self.data.get('body'))
        self.assertEqual(comment, saved_comment)
