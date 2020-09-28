'''
from rest_framework import serializers
from api.v1.models import Reward
from datetime import date

class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ('id', 'label', 'created', 'value', 'type', 'units', 'service', 'region', 'created_by')
'''

