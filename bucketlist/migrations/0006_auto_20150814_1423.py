# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0005_auto_20150814_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='dateadded',
            field=models.DateTimeField(verbose_name='dateadded'),
        ),
    ]
