# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-10 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_auto_20170809_2341'),
    ]

    operations = [
        migrations.CreateModel(
            name='FranchiseStoreProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Available Quantitity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='franchise_product', to='store.Product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store')),
            ],
        ),
    ]
