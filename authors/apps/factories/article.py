import factory
from faker import Factory
from django.apps import apps
from . import UserFactory

Article = apps.get_model('article', 'Article')
faker = Factory.create()


class ArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    author = factory.SubFactory(UserFactory)
    title = faker.name()
    description = faker.text()
    body = faker.text()
    image = factory.django.ImageField(color='blue')


