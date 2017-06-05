# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-01 06:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('mem_total', models.CharField(max_length=50)),
                ('disk', models.CharField(max_length=50)),
                ('time', models.DateTimeField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(choices=[('update', 'Update software'), ('cron', 'Cron job running'), ('fix', 'Fix and squish bugs'), ('backup', 'Backup and rsync')], default='backup', max_length=32)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_task', to='fox.Host')),
            ],
        ),
    ]
