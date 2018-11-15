from rest_framework import serializers
from django.apps import apps	
Article = apps.get_model('article', 'Article')
fields = ('id', 'slug', 'tags')

from .relations import TagRelation
TABLE = apps.get_model('article', 'Article')
TAG = apps.get_model('tags', 'Tag')


class TagsSerializer(serializers.ModelSerializer):	
    """ Serializer for the articles table 	
        to return articles and the tags.
    """	

    article = serializers.SerializerMethodField()	
    tags = TagRelation(many=True, required=False)	
    class Meta:
        model = TABLE	
        fields = ['article', 'tags']		
    def get_article(self, instance):	
        return instance.slug


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for the tags model to 
        return the tag and the slug.
    """

    tag = serializers.CharField(required=True)

    class Meta:
	
        model = TAG

        fields = ['tag', 'slug']

    def create(self, validated_data):

        tag, created = TAG.objects.get_or_create(**validated_data)
	
        validated_data['slug'] = tag.slug
        return validated_data

class TagCreateSerializer(serializers.Serializer):
    """ Serializer for creating tags.
    """	

    tags = TagRelation(many=True, required=True)