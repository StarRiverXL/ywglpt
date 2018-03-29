#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/06
# Email：
from django.conf.urls import url

from . import views, views2


# 视图函数命名空间
app_name = 'asset'
urlpatterns = [
    url(r'^asset/(?P<option>\w*)/(?P<id>\d*)/$', views.assetmanagement, name='asset'),
    url(r'^asset2/(?P<id>\w+)/$', views2.AssetManageDetail.as_view(), name='asset2'),
]

