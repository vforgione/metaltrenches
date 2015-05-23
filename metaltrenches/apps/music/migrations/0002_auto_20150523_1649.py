# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='bandcamp',
            field=models.URLField(blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='band',
            name='facebook',
            field=models.URLField(blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='band',
            name='twitter',
            field=models.URLField(blank=True, null=True, default=None),
        ),
        migrations.AddField(
            model_name='band',
            name='website',
            field=models.URLField(blank=True, null=True, default=None),
        ),
    ]
