# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-01 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fox', '0008_hosttask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hosttask',
            name='task',
        ),
    ]
