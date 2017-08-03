# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=254, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
