import json

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

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user.token)

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
        self.token = 'token'

        self.create_url = reverse(self.namespace + ':register')
        self.login_url = reverse(self.namespace + ':login')
        self.activate_url = reverse(self.namespace + ':activate', kwargs={'token': self.token})
        self.reset_url = reverse(self.namespace + ':resetpassword')
        self.retrieve_user_url = reverse(self.namespace + ':specific_user')
        self.update_user_url = reverse(self.namespace + ':updateuser', kwargs={'token': self.user.token})
        self.resend_activation_url = reverse(self.namespace + ':resend-activation-email')

    def test_retrieve_logged_in_user(self):
        response = self.client.get(self.retrieve_user_url)

        self.assertEqual(200, response.status_code)

    def test_update_user_api(self):
        response = self.client.put(self.update_user_url, self.user_body, format='json')
        self.assertEqual(200, response.status_code)

    def test_update_user_without_password_field(self):
        body = self.user_body
        body.update({'user': {'password': None}})
        response = self.client.put(self.update_user_url, body, format='json')
        self.assertEqual('Please provide a password', response.data.get('message'))

    def test_reset_password_with_previous_password(self):
        body = {'password': self.user_body.get('user').get('password')}
        response = self.client.put(self.update_user_url, body, format='json')
        self.assertEqual('Your new password can\'t be the same as your old password', response.data.get('message'))

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
        self.assertIsNotNone(json.loads(response.content).get('user').get('token'))
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response3.status_code)
        self.assertEqual(400, response4.status_code)

    def test_activate_user(self):
        self.client.post(self.create_url, self.user_body, format='json')
        user = get_user_model().objects.get(email=self.user_body.get('user').get('email'))
        self.activate_url = reverse(self.namespace + ':activate', kwargs={'token': user.token})
        activate = self.client.get(self.activate_url)

        self.assertEqual(activate.json().get('user').get('message'), 'Your account has already been activated.')
        self.assertEqual(activate.status_code, 200)

        # Deactivate a user and then test activation endpoint
        user.is_activated = False
        user.save()
        activate = self.client.get(self.activate_url)

    
    def test_resend_activation_email(self):
        register = self.client.post(self.create_url, self.user_body, format='json')
        activate = self.client.post(self.resend_activation_url, data={"email":self.user_body.get('user').get('email')}, head={"Content-Type":"application/json"})
        activate_wrong_email_format = self.client.post(self.resend_activation_url, data={"email": "wrong_email_format"}, head={"Content-Type":"application/json"})
        unregistered_email = self.client.post(self.resend_activation_url, data={"email": "unregistered@gmail.com"}, head={"Content-Type":"application/json"})
        self.assertEqual(activate.json().get('user').get('message'), 'Success, an activation link has been re-sent to your email.')
        self.assertEqual(activate.status_code, 200)
        self.assertEqual(activate_wrong_email_format.status_code, 400)
        self.assertEqual(unregistered_email.status_code, 400)
        self.assertEqual(activate_wrong_email_format.json().get('errors').get('email')[0], 'Sorry, please enter a valid email address.')
        self.assertEqual(unregistered_email.json().get('errors')[0], "Sorry, that email account is not registered on Authors' Haven")

    def test_reset_password(self):
        register = self.client.post(self.create_url, self.user_body, format='json')
        activate = self.client.post(self.reset_url, data={"email":self.user_body.get('user').get('email')}, head={"Content-Type":"application/json"})
        self.assertEqual(activate.json().get('user').get('message'), 'An email has been sent to your account')
        self.assertEqual(activate.status_code, 200)
