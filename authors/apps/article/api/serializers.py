"""Profile app serializers."""

from rest_framework import serializers
from django.apps import apps
from django.db.models import Avg
from django.contrib.auth.models import AnonymousUser
from authors.apps.profile.api.serializers import ProfileListSerializer
from authors.apps.report.api.serializers import ReportSerializer
from ...core.upload import uploader
from ...tags.api.relations import TagRelation
from authors.apps.notifications.api.views import notify_followed_user_posts_article
import readtime

TABLE = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')
Rating = apps.get_model('rating', 'Rating')
Readers = apps.get_model('read_stats', 'Readers')
TAG = apps.get_model('tags', 'Tag')
Highlights = apps.get_model('highlights', 'Highlights')

NAMESPACE = 'article_api'
fields = ('id', 'slug', 'image', 'title', 'description', 'body', 'user')


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer."""

    update_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':update', lookup_field='slug')
    delete_url = serializers.HyperlinkedIdentityField(
        view_name=NAMESPACE + ':delete', lookup_field='slug')
    author = serializers.SerializerMethodField(read_only=True)
    image_file = serializers.ImageField(required=False)
    favorited = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField(read_only=True)
    disliked_by = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    reading_time = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    dislike_count = serializers.SerializerMethodField(read_only=True)
    my_highlights = serializers.SerializerMethodField(read_only=True)
    read_count = serializers.SerializerMethodField(read_only=True)
    tags = TagRelation(many=True, required=False)

    class Meta:
        """Metadata description."""

        model = TABLE
        fields = fields + (
            'author', 'favorited',
            'favorites_count', 'liked_by',
            'disliked_by', 'image_file', 'rating',
            'update_url', 'delete_url', 'reading_time', 'like_count', 'dislike_count', 'my_highlights', 'read_count', 'tags',)

    def get_favorited(self, obj):
        """Get favourited."""
        user = self.context['request'].user
        return True if obj.is_favorited(user) > 0 else False

    def get_favorites_count(self, obj):
        """Get favourited count."""
        return obj.is_favorited()

    def get_liked_by(self, obj):
        """Get users following."""
        data = obj.liked_by.all().values_list('user__username', flat=True)
        return data

    def get_disliked_by(self, obj):
        """Get users followers."""
        data = obj.disliked_by.all().values_list('user__username', flat=True)
        return data

    def get_reading_time(self, obj):
        """Get reading time."""
        return str(readtime.of_text(obj.body))

    def get_read_count(self, obj):
        """Get number of reads."""
        return Readers.objects.filter(article=obj).count()

    def get_author(self, obj):
        """Get article author."""
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except Profile.DoesNotExist:
            return {}

    def get_like_count(self, obj):
        """Get the number of likes for the article."""
        return obj.liked_by.all().count()

    def get_dislike_count(self, obj):
        """Get the dislike count for an article."""
        return obj.disliked_by.all().count()

    def get_my_highlights(self, obj):
        """Get my highlights for this article."""
        request = self.context.get('request')
        if isinstance(request.user, AnonymousUser):
            return []
        return Highlights.objects.filter(article=obj, author=request.user.profile).values('highlight', 'comment', 'slug')

    def get_rating(self, obj):
        """Get article rating."""
        average = Rating.objects.filter(
            article__pk=obj.pk).aggregate(Avg('your_rating'))
        return average['your_rating__avg']

    def update(self, instance, validated_data):
        """Update article."""
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        if validated_data.get('image_file'):
            image = uploader(validated_data.get('image_file'))
            instance.image = image.get('secure_url', instance.image)

        instance.save()

        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(required=False)
    tags = TagRelation(many=True, required=False,
                       allow_null=True, default=None)

    class Meta:
        model = TABLE

        fields = fields + ('image_file', 'tags',)

    def create(self, validated_data):
        image = None
        request = self.context.get('request')
        if validated_data.get('tags'):

            tags = validated_data.get('tags')
            validated_data.pop('tags')
            instance = TABLE.objects.create(**validated_data)
            for tag in tags:
                t, created = TAG.objects.get_or_create(tag=tag)
                instance.tags.add(t)
            validated_data['tags'] = instance.tags
            validated_data['slug'] = instance.slug
            return validated_data

        else:
            validated_data.pop('tags')
            instance = TABLE.objects.create(**validated_data)

        validated_data['tags'] = instance.tags
        validated_data['slug'] = instance.slug
        if validated_data.get('image_file'):
            image = uploader(validated_data.get('image_file'))
            image = image.get('secure_url')
            del validated_data['image_file']

        validated_data.pop('tags')
        instance = TABLE.objects.create(**validated_data)
        for profile in request.user.profile.followers.all():
            notify_followed_user_posts_article(
                article=instance, follower=profile, request=request)
        instance.image = image if image else None
        instance.save()
        validated_data['slug'] = instance.slug
        validated_data['image'] = instance.image
        validated_data['tags'] = instance.tags
        return validated_data


class ListLikersArticleSerializer(serializers.ModelSerializer):
    """List likers serializer."""

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


class ReportedArticleSerializer(serializers.ModelSerializer):
    """Show all reported articles and the report messages and categories"""

    author = serializers.SerializerMethodField(read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:

        model = TABLE
        fields = ('author', 'title', 'slug', 'reports',)

    def get_author(self, obj):
        return obj.user.username
