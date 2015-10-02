# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0021_auto_20150908_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='auth_key',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='user_id',
            field=models.CharField(max_length=128, blank=True, null=True, default='114388032679125757664'),
        ),
    ]
