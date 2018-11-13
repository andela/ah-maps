from django.test import TestCase
from django.apps import apps
from ...factories import RatingFactory

Rating = apps.get_model('rating', 'Rating')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.data = {
            'your_rating': 4,
        }

    def test_model_can_create_rating(self):
        your_rating = RatingFactory(your_rating=self.data.get('your_rating'))
        saved_rating = Rating.objects.get(your_rating=self.data.get('your_rating'))
        self.assertEqual(your_rating, saved_rating)
