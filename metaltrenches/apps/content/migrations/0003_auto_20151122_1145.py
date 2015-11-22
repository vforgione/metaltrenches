# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20151120_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='subjects',
            field=models.ManyToManyField(related_name='reviews', to='content.ReviewItem'),
        ),
    ]
