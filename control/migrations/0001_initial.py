# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MusicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_id', models.CharField(default='init', max_length=180)),
                ('music_name', models.CharField(default='init', max_length=32)),
                ('artist', models.CharField(default='init', max_length=32)),
                ('album', models.CharField(default='init', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MusicTagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_id', models.CharField(default='init', max_length=180)),
                ('tag', models.CharField(default='init', max_length=32)),
            ],
        ),
    ]