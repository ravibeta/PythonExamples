# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('guid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('callbackurl', models.CharField(max_length=120, editable=False)),
                ('callbackauth', models.CharField(max_length=120, editable=False)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ResourceLease',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('expires', models.DateTimeField(editable=False)),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=2, editable=False)),
                ('reminders', models.IntegerField(default=b'0', editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('term', models.IntegerField(default=b'120', help_text=b'Allowed value should be 0 to 365', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(365)])),
                ('resource', models.ForeignKey(to='api.Resource')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ResourceSubscribers',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('resource', models.ForeignKey(to='api.Resource')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('name', models.CharField(help_text=b'Only lowercase alphabets, numbers are allowed', max_length=80, null=True)),
                ('email', models.CharField(help_text=b'Only email address is allowed', max_length=80, serialize=False, primary_key=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='resourcesubscribers',
            name='subscriber',
            field=models.ForeignKey(to='api.Subscriber'),
        ),
    ]
