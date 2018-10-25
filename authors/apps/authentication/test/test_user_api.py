from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import UserFactory
from django.contrib.auth import get_user_model

#This creates an instance of the factory used to make mock data
faker = Factory.create()

class UserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

        self.namespace = 'authentication'
        self.body = {
            "user": {
                'username': faker.first_name(),
                'email': faker.email(),
                'password': faker.password()
            }
        }
        self.user_body = {
            'user': {
                'username': self.user.username,
                'email': self.user.email,
                'password': '1234abcd'
            }
        }
        self.not_exist= {
             "user": {
                'username': faker.first_name(),
                'email': faker.email(),
                'password': faker.password()
            }
        }
        self.no_username= self.body.update({'username':''})
        self.no_email= self.body.update({'email':''})
        self.email_format= self.body.update({'email':'emailformat'})
        self.password_length= self.body.update({'password':'pass'})

        self.create_url = reverse(self.namespace + ':register')
        self.login_url = reverse(self.namespace + ':login')


    def test_create_user_api(self):

        response = self.client.post(self.create_url, self.body, format='json')
        response2 = self.client.post(self.create_url, self.body, format='json')
        response3 = self.client.post(self.create_url, self.no_username, format='json')
        response4 = self.client.post(self.create_url, self.no_email, format='json')
        response5 = self.client.post(self.create_url, self.email_format, format='json')
        response6 = self.client.post(self.create_url, self.password_length, format='json')

        self.assertEqual(201, response.status_code)
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)
        self.assertEqual(400, response5.status_code)
        self.assertEqual(400, response6.status_code)

    def test_user_login(self):
        register= self.client.post(self.create_url, self.body, format='json')
        response = self.client.post(self.login_url, self.user_body, format='json')
        response2 = self.client.post(self.login_url, self.no_email, format='json')
        response3 = self.client.post(self.login_url, self.no_username, format='json')
        response4 = self.client.post(self.login_url, self.not_exist, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)
