from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import AnonymousUser
from authors.apps.profile.api.serializers import ProfileListSerializer

TABLE = apps.get_model('comment', 'Comment')
CommentHistory = apps.get_model('comment', 'CommentHistory')
Article = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')
User = apps.get_model('authentication', 'User')

NAMESPACE = 'comment_api'
fields = ('id', 'body', 'user', 'thread',)


class CommentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentHistory
        fields = ('body', 'created_at')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TABLE

        fields = fields + ('author',)

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except:
            return {}

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        return instance


class ThreadSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        comment_details = self.parent.parent.__class__(
            value, context=self.context)
        return comment_details.data

    class Meta:
        model = TABLE
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(many=True, read_only=True)
    history = CommentHistorySerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    disliked = serializers.SerializerMethodField(read_only=True)
    dislikes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TABLE

        fields = fields + (
            'author',
            'liked',
            'likes_count',
            'disliked',
            'dislikes_count',
            'history',
        )

    def get_liked(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None
        try:
            obj.likes.get(profile=user.profile)
            return True
        except User.DoesNotExist:
            return False

    def get_likes_count(self, obj):
        return obj.get_likes()

    def get_disliked(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None
        try:
            obj.dislikes.get(profile=user.profile)
            return True
        except User.DoesNotExist:
            return False

    def get_dislikes_count(self, obj):
        return obj.get_dislikes()

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except:
            return {}

    def create(self, validated_data):
        parent = self.context.get('parent', None)
        if parent:
            instance = TABLE.objects.create(parent=parent, **validated_data)
            return instance
        else:
            TABLE.objects.create(**validated_data)
            return validated_data
