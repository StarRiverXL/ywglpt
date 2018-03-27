#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017//
# Email：
from django.conf.urls import url
from . import views

# 视图函数命名空间
app_name = 'ywdocument'
urlpatterns = [
    # url(r'^index/$', views.index, name='index'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/(?P<page>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^search/$', views.search, name='search'),
]


