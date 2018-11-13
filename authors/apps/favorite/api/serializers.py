from rest_framework import serializers
from django.apps import apps
from ...article.api.serializers import ArticleSerializer

Article = apps.get_model('article', 'Article')

fields = ('id', 'slug', 'favorites')


class FavoriteArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article

        fields = fields

    def update(self, instance, validated_data):
        instance.favorites.add(self.context['request'].user)
        instance.save()

        return instance


class FavoriteArticleListSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Article

        fields = ['articles']

    def get_articles(self, obj):
        try:
            serializer = ArticleSerializer(instance=Article.objects.get(id=obj.id), context=self.context)

            return serializer.data
        except:
            return {}
