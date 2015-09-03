# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0010_auto_20150815_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
