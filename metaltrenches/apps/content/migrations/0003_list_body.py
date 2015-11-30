# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151126_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='body',
            field=models.TextField(blank=True, default=''),
        ),
    ]
