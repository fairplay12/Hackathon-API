# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sportsection',
            name='max_ppl_in_section',
            field=models.PositiveSmallIntegerField(default=15),
        ),
    ]
