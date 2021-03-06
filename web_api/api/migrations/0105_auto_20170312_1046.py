# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0104_abp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='key',
            field=models.ForeignKey(db_column=b'_key', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.Key'),
        ),
        migrations.AlterField(
            model_name='point',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
