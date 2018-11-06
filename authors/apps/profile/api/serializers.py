from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model
from versatileimagefield.serializers import VersatileImageFieldSerializer

TABLE = apps.get_model('profile', 'Profile')
APP = 'profile_api'
fields = ('image', 'bio',)
User = get_user_model()

class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes='person_headshot'
    )
    followers = serializers.SerializerMethodField()

    class Meta:
        model = TABLE

        fields = fields + ('username', 'following', 'followers')

    def get_username(self, obj):
        return obj.user.username

    def get_following(self, obj):
        data = []
        for i in obj.is_following.all():
            data.append(i.user.username)
        return data

    def get_followers(self, obj):
        data = []
        for i in obj.followers.all():
            data.append(i.user.username)
        return data

class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TABLE

        fields = fields

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        if validated_data.get('image'):
            instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance
