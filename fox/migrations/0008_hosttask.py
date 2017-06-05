# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-01 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fox', '0007_auto_20170601_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_task', to='fox.Host')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fox.Task')),
            ],
        ),
    ]
