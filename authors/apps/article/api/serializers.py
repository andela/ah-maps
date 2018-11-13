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
    image_file = serializers.ImageField(required=False)
    favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = TABLE

        fields = fields + ('author', 'favorited', 'favorites_count', 'image_file', 'update_url', 'delete_url')

    def get_favorited(self, obj):
        user = self.context['request'].user
        return True if obj.is_favorited(user) > 0 else False

    def get_favorites_count(self, obj):
        return obj.is_favorited()

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except:
            return {}

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        if validated_data.get('image_file'):
            image = uploader(validated_data.get('image_file'))
            instance.image = image.get('secure_url', instance.image)

        instance.save()

        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(required=False)

    class Meta:
        model = TABLE

        fields = fields + ('image_file',)

    def create(self, validated_data):
        image = None
        if validated_data.get('image_file'):
            image = uploader(validated_data.get('image_file'))
            image = image.get('secure_url')
            del validated_data['image_file']
        instance = TABLE.objects.create(**validated_data)
        instance.image = image if image else None
        instance.save()
        validated_data['slug'] = instance.slug
        validated_data['image'] = instance.image
        return validated_data

