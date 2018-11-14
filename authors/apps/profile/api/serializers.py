from rest_framework import serializers
from django.apps import apps
from django.contrib.auth import get_user_model
from ...core.upload import uploader

TABLE = apps.get_model('profile', 'Profile')
APP = 'profile_api'
fields = ('image', 'bio',)
User = get_user_model()
# Readers = apps.get_model('read_stats', 'Readers')


class ProfileListSerializer(serializers.ModelSerializer):
    """List the profiles."""
    username = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    # read_articles = serializers.SerializerMethodField()

    class Meta:
        """Define the serializer META data."""

        model = TABLE
        fields = fields + ('username', 'following', 'followers', )

    def get_username(self, obj):
        """Get users username."""
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_following(self, obj):
        """Get users following."""
        data = obj.is_following.all().values('user__username', 'image')
        return data

    def get_followers(self, obj):
        """Get users followers."""
        data = obj.followers.all().values('user__username', 'image')
        return data

    # def get_read_articles(self, obj):
    #     """Get all the articles I have read."""
    #     return Readers.objects.filter(reader=obj).values('article__title', 'article__slug').distinct()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(required=False)

    class Meta:
        model = TABLE

        fields = fields + ('image_file',)

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        if validated_data.get('image_file'):
            image = uploader(validated_data.get('image_file'))
            instance.image = image.get(
                'secure_url') if image else instance.image
        instance.save()

        return instance


class ProfileFollowSerializer(serializers.ModelSerializer):
    """Profile following/unfollowing serializer."""

    username = serializers.RegexField(
        regex="^(?!.*\ )[A-Za-z\d\-\_][^\W_]+$",
        min_length=3,
        required=True,
        error_messages={
            'invalid': 'Sorry, invalid username. No spaces or special characters allowed.',
            'required': 'Sorry, username is required.',
            'min_length': 'Sorry, username must have at least 3 characters.'
        }

    )

    class Meta:
        """Define the seerializer metadata."""

        model = TABLE

        fields = ['username', ]

    def create(self, validated_data):
        """Follow a profile."""
        # ensure username has not been followed before
        current_profile = self.context.get('request').user.profile
        is_following = current_profile.following(profile=current_profile)
        username = validated_data.get('username')
        # ensure the user exists
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User {} does not exists'.format(username))

        # ensure username has not been followed before
        user = current_profile.is_following.filter(
            user__username__exact=username).values_list('user__username')
        if user:
            raise serializers.ValidationError(
                'You are already following user {}.'.format(username))

        # ensure you don't follow yourself
        current_username = self.context.get('request').user.username
        if current_username == username:
            raise serializers.ValidationError('You cannot follow yourself.')

        # follow
        profile = TABLE.objects.get(user__username=username)
        current_profile.follow(profile)
        return current_profile
