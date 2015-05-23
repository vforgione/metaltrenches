# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('release_date', models.DateField()),
                ('cover_art', models.ImageField(upload_to='cover-art')),
                ('slug', models.SlugField(unique=True, max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True, max_length=100, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(related_name='albums', to='music.Band'),
        ),
        migrations.AddField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(related_name='albums', to='music.Genre'),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('band', 'title', 'release_date')]),
        ),
    ]
