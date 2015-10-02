# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0018_auto_20150903_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='location_url',
            field=models.CharField(max_length=128, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='name_url',
            field=models.CharField(max_length=128, default=1),
            preserve_default=False,
        ),
    ]
