# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-25 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='init', max_length=180)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('music_id', models.CharField(default='init', max_length=180)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default='init', max_length=180)),
                ('cookie', models.CharField(default='init', max_length=256)),
                ('user_name', models.CharField(default='init', max_length=32)),
                ('user_pass', models.CharField(default='init', max_length=32)),
            ],
        ),
    ]