# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 22:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelbuddy_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='datehired',
        ),
        migrations.AlterField(
            model_name='trips',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 28, 14, 4, 14, 702000)),
        ),
        migrations.AlterField(
            model_name='trips',
            name='str_date',
            field=models.DateField(default=datetime.datetime(2017, 11, 28, 14, 4, 14, 702000)),
        ),
    ]
