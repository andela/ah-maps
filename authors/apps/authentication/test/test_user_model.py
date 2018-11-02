from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from authors.apps.factories import UserFactory
from django.contrib.auth import get_user_model

# This creates an instance of the factory used to make mock data
faker = Factory.create()

class UserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

        self.namespace = 'authentication'
        self.body = {
            'username': faker.first_name(),
            'email': faker.email(),
            'password': faker.password()            
        }

    def test_create_user(self):
        self.assertIsInstance(
            get_user_model().objects.create_user(**self.body), get_user_model())
   
    def test_create_super_user(self):
        user = get_user_model().objects.create_superuser(**self.body)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
