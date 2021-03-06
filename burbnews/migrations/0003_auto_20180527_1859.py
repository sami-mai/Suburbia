# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('burbnews', '0002_topic_suburb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='suburb',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local', to='suburb.Suburb'),
        ),
        migrations.AlterField(
            model_name='topicmember',
            name='suburb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='residents', to='suburb.Suburb'),
        ),
    ]
