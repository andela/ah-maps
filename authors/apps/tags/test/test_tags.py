from django.test import TestCase
from django.urls import reverse	
from rest_framework.test import APIClient
from faker import Factory

from ...factories import ArticleFactory, UserFactory
faker = Factory.create()

class TagApiTest(TestCase):
    """ Tag API Test Case
    """

    def setUp(self):	
        self.user = UserFactory()	
        self.article = ArticleFactory()
        self.client = APIClient()	
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)	
        self.tag_namespace = 'tag_api'	
        self.article_namespace = 'article_api'
        self.body = {
            'title': faker.name(),
            'description': faker.text(),	
            'body': faker.text(),
            'tags':["testtag","anothertesttag"]
        }
        self.tags = {	
            'tags':["tag2","tag3"]
        }
        self.stringtag = {	
            "tags":"tag2"	
        }
        self.independent_tag = {
             "tag":"tag"
        }
        self.stringtagbody ={
            'title': faker.name(),
            'description': faker.text(),
            'body': faker.text(),
            'tags':"testtag"
        }
        self.create_url = reverse(self.article_namespace + ':create')
        self.get_tags_url = reverse(self.tag_namespace + ':list')
	
    def test_tag_as_create(self):	
        response = self.client.post(self.create_url, self.body, format='json')	
        self.assertEqual(201, response.status_code)

    def test_tag_existing_article(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.tag_url = reverse(self.tag_namespace + ':create_tags', kwargs={'slug':response.data.get('slug')})
        response2 = self.client.post(self.tag_url, self.tags)
        self.assertEqual(200, response2.status_code)

    def test_string_tag(self):
        response = self.client.post(self.create_url, self.stringtagbody, format='json')
        self.assertEqual(400, response.status_code)

    def test_create_independent_tag(self):
        response = self.client.post(self.get_tags_url, self.independent_tag)
        response2 = self.client.get(self.get_tags_url)
        self.assertEqual(201, response.status_code)
        self.assertEqual(200, response2.status_code)