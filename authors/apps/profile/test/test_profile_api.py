from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import UserFactory

from django.apps import apps

Profile = apps.get_model('profile', 'Profile')

faker = Factory.create()


class ProfileApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = Profile.objects.get(pk=self.user.pk)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.namespace = 'profile_api'
        self.body = {
            'bio': faker.text()
        }
        self.retrieve_url = reverse(self.namespace + ':detail', kwargs={'user__username': self.profile.user.username})
        self.list_url = reverse(self.namespace + ':list')
        self.update_url = reverse(self.namespace + ':update', kwargs={'user__username': self.profile.user.username})

    def test_list_profile_api(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, self.profile)

    def test_retrieve_single_profile_api(self):
        response = self.client.get(self.retrieve_url)
        self.assertContains(response, self.profile)

    def test_update_profile_api(self):
        response = self.client.put(self.update_url, self.body)
        self.assertEqual(200, response.status_code)
