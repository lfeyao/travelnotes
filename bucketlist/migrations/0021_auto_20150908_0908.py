# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0020_remove_place_location_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='album_id',
            field=models.CharField(blank=True, null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='page',
            name='user_id',
            field=models.CharField(blank=True, null=True, max_length=128),
        ),
    ]
