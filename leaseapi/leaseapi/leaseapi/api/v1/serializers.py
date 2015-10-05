from rest_framework import serializers
from api.v1.models import Resource, ResourceLease, Subscriber, ResourceSubscribers
from datetime import date

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'guid')


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('id', 'email')

class ResourceLeaseSerializer(serializers.HyperlinkedModelSerializer):
    resource = ResourceSerializer(read_only=True)
    class Meta:
        model = ResourceLease
        fields = ('id', 'expires', 'term', 'reminders', 'resource')
        read_only_fields = ('id', 'expires', 'term', 'reminders', 'resource') 


class ResourceSubscribersSerializer(serializers.HyperlinkedModelSerializer):
    resource = ResourceSerializer(read_only=True)
    subscriber = SubscriberSerializer
    class Meta:
        model = ResourceSubscribers
        fields = ('id', 'resource', 'subscriber')
        read_only_fields = ('id', 'resource', 'subscriber') 
