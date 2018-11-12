import factory
from faker import Factory
from django.apps import apps
from . import UserFactory

Article = apps.get_model('article', 'Article')
faker = Factory.create()


class ArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    user = factory.SubFactory(UserFactory)
    title = faker.name()
    description = faker.text()
    body = faker.text()
    slug = factory.Sequence(lambda n: 'map-slug%d' % n)
    image = faker.image_url(width=None, height=None)


