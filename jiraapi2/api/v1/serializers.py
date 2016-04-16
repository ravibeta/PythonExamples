from rest_framework import serializers
from .models import JiraRequest

class JiraRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JiraRequest
        fields = ('id', 'sender', 'receiver', 'subject', 'message')
