from django.db import models
from django.db.models import Q
from django.core import validators
from rest_framework import exceptions
import uuid

class LeaseManager(models.Manager):
    
    def get_object(self, pk):
        return super(LeaseManager, self).select_related().get(Q(pk=pk) & ~Q(status='D')) 


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, unique=True)
    callbackurl = models.CharField(max_length=120, null=False, editable=False)
    callbackauth = models.CharField(max_length=120, null=False, editable=False)

    class Meta:
        managed = True
        app_label = 'api'

class ResourceLease(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource)
    expires = models.DateTimeField(null=False,editable=False)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, null=False, editable=False)
    reminders = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(6)], null=False, blank=False, default='0', editable=False)
    TERM_UNIT = 'Days'
    term = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(365)], null=False, blank=False, default='120', help_text='Allowed value should be 0 to 365')
    objects = LeaseManager()
    
    class Meta:
        managed = True
        app_label = 'api'


class Subscriber(models.Model):
    name = models.CharField(max_length=80, null=True, blank=False, help_text='Only lowercase alphabets, numbers are allowed')
    email = models.CharField(max_length=80, null=False, blank=False, primary_key=True, help_text='Only email address is allowed')

    class Meta:
        managed = True
        app_label = 'api'

class ResourceSubscribers(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource)
    subscriber = models.ForeignKey(Subscriber)
    
    class Meta:
        managed = True 
        app_label = 'api'

