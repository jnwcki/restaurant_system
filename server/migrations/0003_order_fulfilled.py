# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20160331_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fulfilled',
            field=models.BooleanField(default=False),
        ),
    ]