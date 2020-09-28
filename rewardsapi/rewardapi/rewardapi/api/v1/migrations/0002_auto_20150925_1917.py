# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Resource',
        ),
        migrations.RemoveField(
            model_name='resourcelease',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcesubscribers',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='resourcesubscribers',
            name='subscriber',
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
        migrations.DeleteModel(
            name='ResourceLease',
        ),
        migrations.DeleteModel(
            name='ResourceSubscribers',
        ),
    ]
