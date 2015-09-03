# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0017_auto_20150901_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_url',
            field=models.CharField(max_length=128, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='category_url',
            field=models.CharField(max_length=128, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='name_url',
            field=models.CharField(max_length=128, default=1),
            preserve_default=False,
        ),
    ]
