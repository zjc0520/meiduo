# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-29 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181024_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_active',
            field=models.BooleanField(default=False),
        ),
    ]
