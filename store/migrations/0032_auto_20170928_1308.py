# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-28 07:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_auto_20170925_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='store',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
    ]
