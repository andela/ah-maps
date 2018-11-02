from django.test import TestCase
from django.contrib.auth import get_user_model
from ...factories.profile import ProfileFactory, Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        self.data = {
            'bio': 'qwerty',
        }

    def test_model_can_create_profile(self):
        profile = ProfileFactory(bio='qwerty')
        saved_profile = Profile.objects.get(bio=self.data.get('bio'))
        self.assertEqual(profile, saved_profile)
