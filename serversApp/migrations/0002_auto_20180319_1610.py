# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-19 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serversApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appmanagement',
            name='code_state',
            field=models.CharField(choices=[('3', 'stop'), ('4', 'restart'), ('2', 'start'), ('1', 'None')], default='1', max_length=10, verbose_name='操作动作'),
        ),
        migrations.AlterField(
            model_name='appmanagement',
            name='state',
            field=models.CharField(choices=[('2', '停用'), ('1', '启用')], default='1', max_length=2, verbose_name='状态'),
        ),
    ]
