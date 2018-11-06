from rest_framework import serializers
from django.apps import apps
from versatileimagefield.serializers import VersatileImageFieldSerializer

TABLE = apps.get_model('profile', 'Profile')
APP = 'profile_api'
fields = ('image', 'bio',)


class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes='person_headshot'
    )

    class Meta:
        model = TABLE

        fields = ('username', 'email') + fields

    def get_username(self, obj):
        return obj.user.username
    
    def get_email(Self, obj):
        return obj.user.email


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
