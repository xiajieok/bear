# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-05 02:49
from __future__ import unicode_literals

from django.db import migrations, models
import fox.models


class Migration(migrations.Migration):

    dependencies = [
        ('fox', '0010_hosttask_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='hosttask',
            name='status',
            field=models.FloatField(default='1', verbose_name=fox.models.Task),
        ),
    ]