# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20150523_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(to='music.Genre', related_name='albums', blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(unique=True, max_length=200, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='band',
            name='slug',
            field=models.SlugField(unique=True, max_length=100, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, max_length=100, editable=False, blank=True),
        ),
    ]
