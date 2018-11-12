from rest_framework import serializers
from django.apps import apps
from authors.apps.profile.api.serializers import ProfileListSerializer
from ...core.upload import uploader

TABLE = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')

NAMESPACE = 'article_api'
fields = ('id', 'slug', 'image', 'title', 'description', 'body', 'user',)


class ArticleSerializer(serializers.ModelSerializer):
    update_url = serializers.HyperlinkedIdentityField(view_name=NAMESPACE + ':update', lookup_field='slug')
    delete_url = serializers.HyperlinkedIdentityField(view_name=NAMESPACE + ':delete', lookup_field='slug')
    author = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TABLE

        fields = fields + ('author', 'image_url', 'update_url', 'delete_url')

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except:
            return {}

    def get_image_url(self, obj):
        return obj.image

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        if validated_data.get('image'):
            image = uploader(validated_data.get('image'))
            instance.image = image.get('secure_url', instance.image)

        instance.save()

        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = TABLE

        fields = fields

    def create(self, validated_data):
        instance = TABLE.objects.create(**validated_data)
        validated_data['slug'] = instance.slug

        if validated_data.get('image'):
            image = uploader(validated_data.get('image'))
            instance.image = image.get('secure_url', instance.image)
            instance.save()
        return validated_data

