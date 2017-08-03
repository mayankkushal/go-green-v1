# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Store')),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone Number')),
                ('slug', models.SlugField()),
            ],
        ),
    ]
