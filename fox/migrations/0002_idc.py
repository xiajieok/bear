# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-28 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fox', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='机房名称')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='机房类型')),
                ('location', models.CharField(blank=True, max_length=30, null=True, verbose_name='机房位置')),
                ('memo', models.TextField(blank=True, max_length=50, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': 'IDC资产信息',
                'verbose_name_plural': 'IDC资产信息管理',
            },
        ),
    ]