# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supportdesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='support_telephone',
            field=models.CharField(default='6101234567', max_length=100),
            preserve_default=False,
        ),
    ]