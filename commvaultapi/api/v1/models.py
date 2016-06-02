from django.db import models
from django.db.models import Q

class BackupRequestManager(models.Manager):

    def get_object(self, pk):
        return super(BackupRequestManager, self).select_related().get(Q(pk=pk) & ~Q(status="D"))

    def get_object_by_user(self, name):
        try:
           backup = super(BackupRequestManager, self).select_related().get(Q(owner=name) & ~Q(status="D"))
        except BackupRequest.DoesNotExist:
           backup = None
        return backup
 
    def get_object_by_server(self, server):
        try:
           backup = super(BackupRequestManager, self).select_related().get(Q(server=server) & ~Q(status="D"))
        except BackupRequest.DoesNotExist:
           backup = None
        return backup

class BackupRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=300, null=True)
    region = models.CharField(max_length=100, null=True)
    platform = models.CharField(max_length=100, null=True)
    server = models.CharField(max_length=100, null=True)
    backup_size = models.IntegerField(null=True, blank=False, default='0', editable=False)
    owner = models.CharField(max_length=50, null=True)#, editable=False)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(null=True, auto_now_add=True)
    status = models.CharField(max_length=2, null=False, default='A', editable=False)
    objects = BackupRequestManager()

    class Meta:
        managed = True
        app_label = 'api'
        db_table = 'backup_images'

'''
CREATE TABLE `backup_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `location` varchar(50) NULL,
  `region` varchar(50) NOT NULL,
  `platform` varchar(50) NOT NULL,
  `server` varchar(100) NOT NULL,
  `backup_size`   int(11) NOT NULL,
  `owner` varchar(50) NULL,
  `status` char(2) NOT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
'''
