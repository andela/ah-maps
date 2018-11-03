import os
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class SocialAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.namespace = 'authentication'

        self.social_auth_url = reverse(self.namespace + ':social')
        self.test_social_body = {
            "provider":"facebook",
            "access_token":os.getenv('facebook_token')
        }
        self.test_google_body= {
            "provider":"google-oauth2",
            "access_token":os.getenv('google_token')
            }
        self.test_twitter_body= {
            "provider":"twitter",
            "access_token":os.getenv('twitter_access_token'),
            "access_token_secret":os.getenv('twitter_access_secret')
        }

    def test_social_auth_api(self):
        pass
        # facebookresponse = self.client.post(self.social_auth_url, self.test_social_body, format='json')
        # twitterresponse = self.client.post(self.social_auth_url, self.test_twitter_body, format='json')
        # googleresponse =self.client.post(self.social_auth_url, self.test_google_body, format='json')

        # self.assertEqual(201, facebookresponse.status_code)
        # self.assertEqual(201, twitterresponse.status_code)
        # self.assertEqual(201, googleresponse.status_code)

