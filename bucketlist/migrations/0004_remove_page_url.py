# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0003_page_was_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='url',
        ),
    ]
