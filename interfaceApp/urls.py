#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 
# Email：
from django.conf.urls import url

from . import views

# 视图函数命名空间
app_name = 'interface'
urlpatterns = [
    url(r'^wenming/$', views.wenming, name='wenming'),    # 用户登陆
    url(r'^pxy/(?P<table>\w*)/$', views.pxy, name='pxy'),
]
