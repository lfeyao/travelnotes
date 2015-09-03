# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0004_remove_page_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='views',
        ),
        migrations.AddField(
            model_name='page',
            name='dateadded',
            field=models.DateField(default=datetime.datetime(2015, 8, 14, 17, 8, 11, 475488, tzinfo=utc), verbose_name='dateadded'),
            preserve_default=False,
        ),
    ]
