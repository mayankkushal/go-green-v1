# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-25 14:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0030_productcategory_parent_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_staff', models.CharField(choices=[('I', 'Inventory Manager'), ('B', 'Billing Clerk')], max_length=1)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staffs',
            },
        ),
        migrations.AddField(
            model_name='franchise',
            name='mgr_password',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Manager Password'),
        ),
        migrations.AddField(
            model_name='store',
            name='mgr_password',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Manager Password'),
        ),
        migrations.AddField(
            model_name='staff',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='store.Store'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='store_staff', to=settings.AUTH_USER_MODEL),
        ),
    ]
