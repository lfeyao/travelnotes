# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0019_auto_20150903_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='location_url',
        ),
    ]
