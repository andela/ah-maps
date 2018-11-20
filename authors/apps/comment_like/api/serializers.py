from rest_framework import serializers
from django.apps import apps

Comment = apps.get_model('comment', 'Comment')

fields = ('id', 'body',)


class LikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

        fields = fields

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.get_likes(user) > 0:
            instance.likes.remove(user)
        else:
            instance.likes.add(user)
            if instance.get_dislikes(user):
                instance.dislikes.remove(user)
        instance.save()

        return instance


class DisLikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

        fields = fields

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.get_dislikes(user) > 0:
            instance.dislikes.remove(user)
        else:
            instance.dislikes.add(user)
            if instance.get_likes(user):
                instance.likes.remove(user)
        instance.save()

        return instance
