# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='special_instructions',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
