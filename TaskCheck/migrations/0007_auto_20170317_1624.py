# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskCheck', '0006_auto_20170317_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='活动？'),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='活动？'),
        ),
    ]
