# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-28 09:56
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suburb', '0010_suburb_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suburb',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='suburb',
            name='suburb_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
