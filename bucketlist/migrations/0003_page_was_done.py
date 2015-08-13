# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0002_auto_20150812_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='was_done',
            field=models.BooleanField(default=False),
        ),
    ]
