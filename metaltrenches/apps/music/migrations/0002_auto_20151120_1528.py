# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, editable=False, blank=True)),
                ('release_date', models.DateField()),
                ('cover_art', models.ImageField(upload_to='cover-art', null=True, default=None, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, editable=False, blank=True)),
                ('picture', models.ImageField(upload_to='band-pictures', null=True, default=None, blank=True)),
                ('website', models.URLField(null=True, default=None, blank=True)),
                ('facebook', models.URLField(null=True, default=None, blank=True)),
                ('twitter', models.URLField(null=True, default=None, blank=True)),
                ('bandcamp', models.URLField(null=True, default=None, blank=True)),
                ('itunes', models.URLField(null=True, default=None, blank=True)),
                ('playstore', models.URLField(null=True, default=None, blank=True)),
                ('amazon', models.URLField(null=True, default=None, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(null=True, default=None, blank=True, max_length=255)),
                ('slug', models.SlugField(unique=True, editable=False, blank=True)),
                ('date', models.DateTimeField(default=None, blank=True, null=True)),
                ('location', models.CharField(null=True, default=None, blank=True, max_length=500)),
                ('more_info', models.TextField(default=None, blank=True, null=True)),
                ('picture', models.ImageField(upload_to='event-pictures', null=True, default=None, blank=True)),
                ('bands', models.ManyToManyField(related_name='events', to='music.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, editable=False, blank=True)),
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
            field=models.ManyToManyField(related_name='albums', blank=True, to='music.Genre'),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('band', 'title')]),
        ),
    ]
