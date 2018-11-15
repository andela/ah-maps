from rest_framework import serializers
from django.apps import apps
from django.db.models import Avg

TABLE = apps.get_model('report', 'Report')
fields = ('user', 'message', 'category',)

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TABLE

        fields = '__all__'




