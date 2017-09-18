# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-18 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0019_bill_editable'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='return_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
