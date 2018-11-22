import factory
from faker import Factory
from django.apps import apps
from . import UserFactory, ArticleFactory

Comment = apps.get_model('comment', 'Comment')
faker = Factory.create()


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    article = factory.SubFactory(ArticleFactory)
    body = faker.text()
