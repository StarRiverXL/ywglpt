#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/06
# Email：
from django.conf.urls import url

from . import views

# 视图函数命名空间
app_name = 'servers'
urlpatterns = [
    url(r'^serveropt/$', views.serveropt, name='serveropt'),    # 服务日志管理
    url(r'^appopt/(?P<option>\w*)/$', views.appopt, name='appopt'),     # 服务管理
    url(r'^downloadlog/$', views.download_file, name='downloadlog')     # 日志下载
]
