# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-02 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0090_auto_20161202_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lorawanapplication',
            name='api_key',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
