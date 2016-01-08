'''
from rest_framework import serializers
from api.v1.models import Metric
from datetime import date

class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ('id', 'label', 'created', 'value', 'type', 'units', 'service', 'region', 'created_by')
'''

