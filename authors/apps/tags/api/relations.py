
import re	
from rest_framework import serializers
from django.utils.text import slugify	
from ..models import Tag

class TagRelation(serializers.RelatedField):
    """
         Provides the relationship between tag objects 
         and the article	
    """
    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):	
        return value.tag
	
    def to_internal_value(self, data):

        if not re.match(r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$', data):
            raise serializers.ValidationError('Tag cannot have special characters')	
            
        tag, created = Tag.objects.get_or_create(tag=data)
        return tag