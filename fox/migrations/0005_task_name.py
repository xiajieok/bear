# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-01 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fox', '0004_auto_20170601_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='cron', max_length=32),
        ),
    ]