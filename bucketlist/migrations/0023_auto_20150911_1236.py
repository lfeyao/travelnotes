# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0022_auto_20150908_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name_url',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='category_url',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='country',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='name_url',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='name_url',
            field=models.CharField(max_length=128, blank=True, null=True),
        ),
    ]
