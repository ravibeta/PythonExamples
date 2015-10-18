from django.db import models
from django.forms import ModelForm

LANDSCAPE_CHOICES = (
    ('DEV', 'Dev'),
    ('TEST', 'Test'),
    ('PROD', 'Prod'),
)

class Reminder(models.Model):
    purpose = models.CharField(max_length=100, default='purpose')
    #landscape = models.CharField(max_length=3, choices=LANDSCAPE_CHOICES)
    subscriber = models.CharField(max_length=100, null=False, blank=False, default='rajamani@adobe.com')
    term = models.IntegerField(null=False, blank=False, default='0', help_text='denotes the lapse for the next reminder')

class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        fields = ['purpose',  'subscriber', 'term']

