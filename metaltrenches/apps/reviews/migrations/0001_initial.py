# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('score', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('album', models.ForeignKey(related_name='ratings', to='music.Album')),
            ],
        ),
        migrations.CreateModel(
            name='RatingFactor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('subtitle', models.CharField(max_length=100, default=None, null=True, blank=True)),
                ('body', models.TextField(default='', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
                ('published', models.DateTimeField(default=None, null=True, blank=True)),
                ('album', models.ForeignKey(related_name='reviews', to='music.Album')),
                ('author', models.ForeignKey(related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='factor',
            field=models.ForeignKey(to='reviews.RatingFactor'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('album', 'factor')]),
        ),
    ]
