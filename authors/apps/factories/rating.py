import factory
from faker import Factory
from django.apps import apps
import random
from . import UserFactory, ArticleFactory

Rating = apps.get_model('rating', 'Rating')
faker = Factory.create()


class RatingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Rating

    user = factory.SubFactory(UserFactory)
    your_rating = faker.random
    article = factory.SubFactory(ArticleFactory)


