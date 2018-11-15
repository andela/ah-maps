from django.test import TestCase	
from django.apps import apps
from ...factories.tag import TagFactory, Tag

class TagModelTest(TestCase):

    def setUp(self):	
        self.data = {	
            'tag': 'yaaay',
        }

    def test_model_can_create_tag(self):
        tag = TagFactory(tag=self.data.get('tag'))
        saved_tag = Tag.objects.get(tag=self.data.get('tag'))	
        self.assertEqual(tag, saved_tag)