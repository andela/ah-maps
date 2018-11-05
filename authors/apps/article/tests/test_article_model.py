from django.test import TestCase
from django.apps import apps
from ...factories import ArticleFactory

Article = apps.get_model('article', 'Article')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.data = {
            'title': 'this is a title',
        }

    def test_model_can_create_profile(self):
        article = ArticleFactory(title=self.data.get('title'))
        saved_article = Article.objects.get(title=self.data.get('title'))
        self.assertEqual(article, saved_article)
