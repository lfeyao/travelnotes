# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0015_auto_20150831_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='category',
            field=models.CharField(max_length=10, choices=[('Eat', 'Eat'), ('See', 'See'), ('Sleep', 'Sleep')]),
        ),
    ]
