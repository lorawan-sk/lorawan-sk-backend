# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 09:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20160301_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='gw',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Gateway'),
        ),
        migrations.AlterField(
            model_name='point',
            name='key',
            field=models.ForeignKey(db_column=b'_key', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.Key'),
        ),
        migrations.AlterField(
            model_name='point',
            name='node',
            field=models.ForeignKey(db_column=b'serial', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.Node'),
        ),
    ]
