# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_apikey'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]