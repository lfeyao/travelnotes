# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0013_auto_20150830_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='places_to_eat',
        ),
        migrations.RemoveField(
            model_name='page',
            name='places_to_visit',
        ),
        migrations.AlterField(
            model_name='place',
            name='category',
            field=models.CharField(choices=[('Eat', 'Eat'), ('See', 'See'), ('Sleep', 'Sleep')], max_length=1),
        ),
    ]
