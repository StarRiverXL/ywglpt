# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-21 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serversApp', '0003_auto_20180320_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appmanagement',
            name='code_state',
            field=models.CharField(choices=[('3', 'stop'), ('4', 'restart'), ('2', 'start'), ('1', 'None')], default='1', max_length=10, verbose_name='操作动作'),
        ),
    ]
