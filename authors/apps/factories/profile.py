import factory
from faker import Factory
from django.apps import apps
from django.db.models import signals
from . import UserFactory

Profile = apps.get_model('profile', 'Profile')
faker = Factory.create()


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = faker.text()
    image = factory.django.ImageField(color='blue')


