# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-28 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20170528_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile-picture', verbose_name='Profile Picture'),
        ),
    ]
