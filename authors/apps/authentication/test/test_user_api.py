from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import UserFactory

#This creates an instance of the factory used to make mock data
faker = Factory.create()


class UserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.namespace = 'authentication'
        self.body = {
            "user": {
            'username': faker.first_name(),
            'email': faker.email(),
            'password': faker.password()
            }
        }
        self.create_url = reverse(self.namespace + ':register')
        self.login_url = reverse(self.namespace + ':login')
       

    def test_create_user_api(self):
        response = self.client.post(self.create_url, self.body, format='json')
        self.assertEqual(201, response.status_code)

    def test_user_login(self):
        self.client.post(self.create_url, self.body, format='json')
        response = self.client.post(self.login_url, self.body, format='json')
        self.assertEqual(200, response.status_code)
            

