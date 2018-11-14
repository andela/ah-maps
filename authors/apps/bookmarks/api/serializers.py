from rest_framework import serializers
from authors.apps.article.api.serializers import TABLE
from authors.apps.profile.api.serializers import ProfileListSerializer
from authors.apps.profile.api.serializers import TABLE as Profile

class BookMarkSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TABLE

        fields = ('author', 'title', 'slug', )

    def get_author(self, obj):
        try:
            serializer = ProfileListSerializer(
                instance=Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except Profile.DoesNotExist:
            return {}
