# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-28 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0020_bill_return_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mgr_access',
            field=models.BooleanField(default=False),
        ),
    ]
