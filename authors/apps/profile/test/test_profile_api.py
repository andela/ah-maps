from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Factory
from ...factories import UserFactory
from ...factories.profile import ProfileFactory

faker = Factory.create()


class ProfileApiTest(TestCase):
    def setUp(self):
        self.profile = ProfileFactory()
        self.user2 = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.profile.user)

        self.namespace = 'profile_api'
        self.body = {
            'bio': faker.text()
        }
        self.retrieve_url = reverse(self.namespace + ':detail', kwargs={'user__username': self.profile.user.username})
        self.list_url = reverse(self.namespace + ':list')
        self.update_url = reverse(self.namespace + ':update', kwargs={'user__username': self.profile.user.username})
        self.update_url_use2 = reverse(self.namespace + ':update', kwargs={'user__username': self.user2.username})
        self.follow_url = reverse(self.namespace + ':follow_unfollow', kwargs={'username': self.user2.username})
        self.get_followers_url = reverse(self.namespace + ':get_followers', kwargs={'username': self.user2.username})
        self.get_following_url = reverse(self.namespace + ':get_followed', kwargs={'username': self.user2.username})
        self.follow_url_non_existent = reverse(self.namespace + ':follow_unfollow', kwargs={'username': "noone"})
        self.follow_yourself_url = reverse(self.namespace + ':follow_unfollow', kwargs={'username': self.profile.user.username})

    def test_list_profile_api(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, self.profile)

    def test_retrieve_single_profile_api(self):
        response = self.client.get(self.retrieve_url)
        self.assertContains(response, self.profile)

    def test_update_other_user_profile_api(self):
        response = self.client.put(self.update_url_use2, self.body)
        self.assertEqual(403, response.status_code)

    def test_update_own_profile_api(self):
        response = self.client.put(self.update_url, self.body)
        self.assertEqual(200, response.status_code)


    def test_follow_user(self):
        res = self.client.post(self.follow_url)
        self.assertEqual(200, res.status_code)

    def test_unfollow_user(self):
        self.client.post(self.follow_url)
        res = self.client.delete(self.follow_url)
        self.assertEqual(200, res.status_code)

    def test_get_followers(self):
        res = self.client.get(self.get_followers_url)
        self.assertEqual(200, res.status_code)

    def test_get_following(self):
        res = self.client.get(self.get_following_url)
        self.assertEqual(200, res.status_code)

    def test_unfollow_someone_you_dont_follow(self):
        self.client.post(self.follow_url_non_existent)
        res = self.client.delete(self.follow_url)
        self.assertEqual(400, res.status_code)

    def test_follow_yourself(self):
        res = self.client.post(self.follow_yourself_url)
        self.assertEqual(400, res.status_code)

    def test_follow_someone_twice(self):
        self.client.post(self.follow_url)
        res =  self.client.post(self.follow_url)
        self.assertEqual(400, res.status_code)
