from rest_framework import serializers, status
from django.apps import apps
from authors.apps.profile.api.serializers import ProfileListSerializer
from authors.apps.article.api.serializers import ArticleSerializer

TABLE = apps.get_model('comment', 'Comment')
Article = apps.get_model('article', 'Article')
Profile = apps.get_model('profile', 'Profile')

NAMESPACE = 'comment_api'
fields = ('id', 'body', 'user', 'thread',)


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
        comment_details = self.parent.parent.__class__(value, context=self.context)
        return comment_details.data

    class Meta:
        model = TABLE
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(many=True, read_only=True)
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

    def create(self, validated_data):
        parent = self.context.get('parent', None)
        if parent:
            instance = TABLE.objects.create(parent=parent, **validated_data)
            return instance
        else:
            TABLE.objects.create(**validated_data)
            return validated_data
