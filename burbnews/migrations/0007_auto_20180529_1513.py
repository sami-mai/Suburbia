# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burbnews', '0006_topicmember_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicmember',
            name='image',
        ),
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='topic_image/'),
        ),
    ]
