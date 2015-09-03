# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0008_auto_20150814_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='datedone',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='dateadded',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
