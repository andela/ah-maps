
import factory	
from faker import Factory
from django.apps import apps

Tag = apps.get_model('tags', 'Tag')	
faker = Factory.create()
	
class TagFactory(factory.DjangoModelFactory):
    """Class to fake sample tags
    """
    class Meta:	
        model = Tag
    tag = faker.text()