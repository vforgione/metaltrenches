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
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(default=None, null=True, blank=True, max_length=255)),
                ('body', models.TextField(default='', blank=True)),
                ('slug', models.SlugField(unique=True, blank=True, max_length=100, editable=False)),
                ('published', models.DateTimeField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RatingFactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(default=None, null=True, blank=True, max_length=255)),
                ('body', models.TextField(default='', blank=True)),
                ('slug', models.SlugField(unique=True, blank=True, max_length=100, editable=False)),
                ('published', models.DateTimeField(default=None, null=True, blank=True)),
                ('is_ordered', models.NullBooleanField(default=None)),
                ('is_ordered_descending', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('object_id', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('sequence', models.IntegerField(default=None, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', default=None, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='subjects',
            field=models.ManyToManyField(to='content.ReviewItem'),
        ),
        migrations.AddField(
            model_name='rating',
            name='factor',
            field=models.ForeignKey(to='content.RatingFactor'),
        ),
        migrations.AddField(
            model_name='rating',
            name='item',
            field=models.ForeignKey(related_name='ratings', to='content.ReviewItem'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('item', 'factor')]),
        ),
    ]
