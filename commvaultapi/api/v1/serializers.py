from rest_framework import serializers
from .models import BackupRequest

class BackupRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BackupRequest
        fields = ('id', 'name', 'location', 'region', 'platform', 'server', 'backup_size', 'owner', 'status', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified', 'status')
