# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-09 15:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0018_store_return_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', models.SlugField(unique=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='Store-picture', verbose_name='Store Image')),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone Number')),
                ('website', models.URLField(default='', max_length=256, verbose_name='Website')),
                ('hours', models.CharField(default='', max_length=256, verbose_name='Hours')),
                ('street', models.CharField(default='', max_length=256, verbose_name='Street')),
                ('city', models.CharField(default='', max_length=256, verbose_name='City')),
                ('state', models.CharField(default='', max_length=256, verbose_name='State')),
                ('postal', models.PositiveIntegerField(default=0, verbose_name='Postal')),
                ('return_days', models.PositiveIntegerField(default=7, verbose_name='Return Days')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='franchise', to='store.Category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='franchise', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='infinite_quantity',
            field=models.BooleanField(default=False, verbose_name='Infinite Quantity'),
        ),
        migrations.AddField(
            model_name='store',
            name='stand_alone',
            field=models.BooleanField(default=True, verbose_name='Is a stand alone store?'),
        ),
        migrations.AlterField(
            model_name='store',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store', to='store.Category'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='franchise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store', to='store.Franchise'),
        ),
    ]
