"""Profile app serializers."""

from rest_framework import serializers
from django.apps import apps
from django.db.models import Avg
from authors.apps.profile.api.serializers import ProfileListSerializer
from ...core.upload import uploader

TABLE = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')
Rating = apps.get_model('rating', 'Rating')

NAMESPACE = 'article_api'
fields = ('id', 'slug', 'image', 'title', 'description',
          'body', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer."""

    update_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':update', lookup_field='slug')
    delete_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':delete', lookup_field='slug')
    author = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False)
    image_url = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField(read_only=True)
    disliked_by = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Metadata description."""

        model = TABLE

        fields = fields + ('author', 'update_url',
                           'delete_url', 'liked_by', 'disliked_by', 'image_url', 'rating')

    def get_liked_by(self, obj):
        """Get users following."""
        data = obj.liked_by.all().values_list('user__username', flat=True)
        return data

    def get_disliked_by(self, obj):
        """Get users followers."""
        data = obj.disliked_by.all().values_list('user__username', flat=True)
        return data

    def get_author(self, obj):
        """Get article author."""
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except Profile.DoesNotExist:
            return {}
    
    def get_rating(self, obj):
        average = Rating.objects.filter(article__pk=obj.pk).aggregate(Avg('your_rating'))
        return average['your_rating__avg']

    def get_image_url(self, obj):
        return obj.image

    def update(self, instance, validated_data):
        """Update article."""
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        if validated_data.get('image'):
            image = uploader(validated_data.get('image'))
            instance.image = image.get('secure_url', instance.image)

        instance.save()

        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Create an article."""
    image = serializers.ImageField(required=False)

    class Meta:
        """Metadata description."""

        model = TABLE

        fields = fields

    def create(self, validated_data):
        """Create article."""
        instance = TABLE.objects.create(**validated_data)
        validated_data['slug'] = instance.slug

        if validated_data.get('image'):
            image = uploader(validated_data.get('image'))
            instance.image = image.get('secure_url', instance.image)
            instance.save()
        return validated_data


class ListLikersArticleSerializer(serializers.ModelSerializer):
    """List likers serializer."""

    # image = serializers.SerializerMethodField(read_only=True)
    liked_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Metadata description."""

        model = TABLE

        fields = ('liked_by',)

    def get_liked_by(self, obj):
        """Get users following."""
        data = obj.liked_by.all().values('user__username', 'image')
        return data


class ListDislikersArticleSerializer(serializers.ModelSerializer):
    """List dislikers serializer."""

    disliked_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Metadata description."""

        model = TABLE

        fields = ('disliked_by',)

    def get_disliked_by(self, obj):
        """Get users followers."""
        data = obj.disliked_by.all().values(
            'user__username', 'image')
        return data
