# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0024_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': (('read_category', 'Can read Category'),)},
        ),
        migrations.AlterField(
            model_name='place',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
