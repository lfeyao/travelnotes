# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0016_auto_20150831_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='dateadded',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='page',
            name='datedone',
        ),
        migrations.RemoveField(
            model_name='page',
            name='picturelink',
        ),
        migrations.AddField(
            model_name='page',
            name='picture_link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='years_visted',
            field=models.CommaSeparatedIntegerField(null=True, blank=True, max_length=200),
        ),
    ]
