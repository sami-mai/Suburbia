# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 13:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suburb', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Residents',
            new_name='Resident',
        ),
        migrations.RenameField(
            model_name='suburb',
            old_name='name',
            new_name='suburb_name',
        ),
    ]
