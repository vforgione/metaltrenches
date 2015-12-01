# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True)),
                ('release_date', models.DateField()),
                ('cover_art', models.ImageField(null=True, default=None, upload_to='cover-art', blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True)),
                ('picture', models.ImageField(null=True, default=None, upload_to='band-pictures', blank=True)),
                ('website', models.URLField(null=True, default=None, blank=True)),
                ('facebook', models.URLField(null=True, default=None, blank=True)),
                ('twitter', models.URLField(null=True, default=None, blank=True)),
                ('bandcamp', models.URLField(null=True, default=None, blank=True)),
                ('itunes', models.URLField(null=True, default=None, blank=True)),
                ('playstore', models.URLField(null=True, default=None, blank=True)),
                ('amazon', models.URLField(null=True, default=None, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(null=True, max_length=255, default=None, blank=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True)),
                ('date', models.DateTimeField(null=True, blank=True, default=None)),
                ('location', models.CharField(null=True, max_length=500, default=None, blank=True)),
                ('more_info', models.TextField(null=True, blank=True, default=None)),
                ('picture', models.ImageField(null=True, default=None, upload_to='event-pictures', blank=True)),
                ('bands', models.ManyToManyField(to='content.Band', related_name='events')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(null=True, max_length=255, default=None, blank=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True, max_length=100)),
                ('published', models.DateTimeField(null=True, blank=True, default=None)),
                ('is_ordered', models.NullBooleanField(default=None)),
                ('is_ordered_descending', models.NullBooleanField(default=None)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('body', models.TextField(blank=True, default='')),
                ('sequence', models.IntegerField(null=True, blank=True, default=None)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('list', models.ForeignKey(to='content.List', related_name='items')),
            ],
            options={
                'ordering': ('list', 'sequence'),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(null=True, max_length=255, default=None, blank=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True, max_length=100)),
                ('published', models.DateTimeField(null=True, blank=True, default=None)),
                ('body', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('score', models.PositiveIntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='RatingFactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(null=True, max_length=255, default=None, blank=True)),
                ('slug', models.SlugField(editable=False, unique=True, blank=True, max_length=100)),
                ('published', models.DateTimeField(null=True, blank=True, default=None)),
                ('body', models.TextField(blank=True, default='')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='rating',
            name='factor',
            field=models.ForeignKey(to='content.RatingFactor'),
        ),
        migrations.AddField(
            model_name='album',
            name='band',
            field=models.ForeignKey(to='content.Band', related_name='albums'),
        ),
        migrations.AddField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(blank=True, to='content.Genre', related_name='albums'),
        ),
    ]
