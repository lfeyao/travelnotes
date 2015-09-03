# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0014_auto_20150830_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='picturelink',
            field=models.CharField(blank=True, null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, null=True, max_length=128),
        ),
    ]
