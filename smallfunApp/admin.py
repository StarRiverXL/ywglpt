#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017//
# Email：
# Register your models here.
from django.contrib import admin
from .models import AddressYunwei


class AddressYunweiAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'position', 'QQ', 'note']

# 把新增的 PostAdmin 也注册进来
admin.site.register(AddressYunwei, AddressYunweiAdmin)

