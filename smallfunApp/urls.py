#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 
# Email： 
from django.conf.urls import url
from . import views

# 视图函数命名空间
app_name = 'samllfun'
urlpatterns = [
    url(r'^address/$', views.address, name='address'),
]








