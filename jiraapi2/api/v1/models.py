from django.db import models
from django.db.models import Q

class JiraRequestManager(models.Manager):

    def get_object(self, pk):
        return super(JiraRequestManager, self).select_related().get(Q(pk=pk) & ~Q(status="D"))

    def get_object_by_sender(self, name):
        try:
           jira = super(JiraRequestManager, self).select_related().get(Q(sender=name) & ~Q(status="D"))
        except JiraRequest.DoesNotExist:
           jira = None
        return jira

    def get_object_by_user(self, name):
        try:
           jira = super(JiraRequestManager, self).select_related().get(Q(user=name) & ~Q(status="D"))
        except JiraRequest.DoesNotExist:
           jira = None
        return jira
 
    def get_object_by_hash(self, digest):
        try:
           jira = super(JiraRequestManager, self).select_related().get(Q(digest_hash=digest) & ~Q(status="D"))
        except JiraRequest.DoesNotExist:
           jira = None
        return jira

class JiraRequest(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.CharField(max_length=100, null=False)
    sender = models.CharField(max_length=100, null=False)
    cc = models.CharField(max_length=100, null=True)
    bcc = models.CharField(max_length=100, null=True)
    subject = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=50, null=True)
    digest_hash = models.CharField(max_length=100, null=False, unique=True, editable=False) # hash of the above fields
    user_name = models.CharField(max_length=50, null=True, editable=False)
    created = models.DateTimeField(null=True, editable=False)
    modified = models.DateTimeField(null=True, auto_now_add=True)
    status = models.CharField(max_length=2, null=False, editable=False)
    objects = JiraRequestManager()

    class Meta:
        managed = True
        app_label = 'api'
