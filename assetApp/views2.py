#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 
# Email： 
from django.views.generic import ListView, DetailView
from .models import AssetManagement

import logging
logger = logging.getLogger('django')


class AssetManageList(ListView):
    logger.info("调用资产管理ListView类视图")
    model = AssetManagement
    context_object_name = 'AssetManageList'
    template_name = 'assetApp/asset_tmp.html'
    
    def get_queryset(self):
        # pk = self.kwargs.get("ip")
        pk = self.kwargs['ip']
        # pk = self.request.GET.get('key')
        AssetManageList2 = AssetManagement.objects.all()[:int(pk)]
        return AssetManageList2

    def get_context_data(self, **kwargs):
        kwargs['my_list'] = AssetManagement.objects.all()[:10]
        kwargs['my_list2'] = self.kwargs.get("ip")
        return super(AssetManageList, self).get_context_data(**kwargs)


class AssetManageDetail(DetailView):
    logger.info("调用资产管理DetailView类视图")
    model = AssetManageList
    context_object_name = 'AsseetManageList'
    template_name = 'assetApp/asset_tmp_detail.html'
    pk_url_kwarg = 'ip'



