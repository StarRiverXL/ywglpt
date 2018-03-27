#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/06
# Email：
from django.db import models
from mptt.models import MPTTModel
# Create your models here.


class AssetManagement(models.Model):
    """
    资产管理
    """
    ip = models.CharField(max_length=15)
    host_name = models.CharField('主机名', max_length=255)
    project = models.CharField('所属项目', max_length=255)
    system = models.CharField('操作系统', max_length=20)
    cpu = models.CharField(max_length=20)
    memory = models.CharField('内存', max_length=20)
    hard = models.CharField('硬盘', max_length=20)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ip






