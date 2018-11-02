import factory
from faker import Factory
from django.contrib.auth import get_user_model

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        
    username = factory.Sequence(lambda n: 'map%d' % n)
    email = factory.Sequence(lambda n: 'example_%s@map.com' % n)
    password = factory.PostGenerationMethodCall('set_password', '1234abcd')
    is_activated = True
