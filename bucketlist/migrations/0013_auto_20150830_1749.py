# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0012_auto_20150815_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('category', models.CharField(max_length=128)),
                ('likes', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='country',
            field=models.CharField(max_length=128, default='United States'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='places_to_eat',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='page',
            name='places_to_visit',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.ForeignKey(to='bucketlist.Page'),
        ),
    ]
