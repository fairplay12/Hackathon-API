# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20171111_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(default=123),
            preserve_default=False,
        ),
    ]