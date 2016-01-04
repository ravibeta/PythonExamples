from django.db import models
from django.db.models import Q
from django.core import validators
from rest_framework import exceptions
import uuid
#import metricapi.wsgi

#class LeaseManager(models.Manager):
#    
#    def get_object(self, pk):
#        return super(LeaseManager, self).select_related().get(Q(pk=pk) & ~Q(status='D')) 


class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50, null=False, default='UNKNOWN')
    created = models.DateTimeField(null=False, auto_now_add=True)
    value = models.FloatField(null=False, default=0)
    type = models.CharField(max_length=50, null=False, default='gauge')
    units = models.CharField(max_length=50, null=False, default='NA')
    service = models.CharField(max_length=50, null=False, default='NA')
    region = models.CharField(max_length=50, null=False, default='NA')
    created_by = models.CharField(max_length=50, null=False, default='NA')

    class Meta:
        managed = True
        app_label = 'api'

