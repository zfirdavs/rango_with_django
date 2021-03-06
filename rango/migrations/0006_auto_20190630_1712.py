# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-06-30 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='rango.Category'),
        ),
    ]
