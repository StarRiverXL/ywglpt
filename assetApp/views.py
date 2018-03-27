#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import AssetManagement
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import logging


logger = logging.getLogger('django')


# @login_required
def assetmanagement(request, option, id):
    """
        资产管理
    : param option: 操作的动作，如 添加、查询、删除等
    : param id: 删除及编辑资产时选择对应的id号，查询时选择没有的资产0
    : return: 返回对应页面及数据
    """
    logger.info("进入资料管理视图,请求参数为: option=[%s],id=[%s]" % (option, id))
    asset_search = request.GET.get('asset_search', '未提交到搜索关键字')     # 获取搜索查询结果
    page = int(request.GET.get('page', 1))      # 获取分页，默认为第一页
    pagenumber = int(request.GET.get('pagenumber', 10))      # 每页展示数量，默认5条
    pagenumber_switch = int(request.GET.get('pagenumber_switch', 0))    # 设置展示行数时的开关
    logger.info("资产管理GET请求提交参数:asset_search=[{0}]、page=[{1}]、pagenumber=[{2}]、pagenumber_switch=[{3}]".format(
        asset_search, page, pagenumber, pagenumber_switch))
    # 设置查询页面刷新参数
    page_condition = {"asset_search": asset_search,
                      "pagenumber": pagenumber,
                      "pagenumber_switch": 0}

    def paginatorlist(content, page, pagenumber):
        """
            资产管理,对结果进行分页,返回当页的所有结果
            content: 数据库查询的内容结果
            page: 获取指定页的数据
            pagenumber: 每页的数量
        """
        logger.info("资产管理,对查询结果进行分页,返回当页的所有结果,传入参数为：page=[{0}]、pagenumber=[{1}]".format(page, pagenumber))
        paginator = Paginator(content, pagenumber)      # 对结果进行分页,每页的分页数量
        try:
            contacts = paginator.page(page)     # 取指定页的数据
        except PageNotAnInteger as e:
            logger.error("资产管理,获取指定页的数据异常,返回第一页结果,异常原因: %s" % e)
            contacts = paginator.page(1)    # 如果用户请求的页码号不是整数，显示第一页
        except EmptyPage:
            logger.error("资产管理,获取指定页的数据异常,用户请求的页码号超过了最大页码号，将显示最后一页")
            contacts = paginator.page(paginator.num_pages)
        logger.info("资产管理,成功返回查询结果")
        return contacts

    if option == "add_asset":
        logger.info('进入资产管理添加页面,请求id为: %s' % int(id))
        if request.method == 'POST' and int(id) == 0:
            logger.info("资产管理,开始添加数据")
            ip = request.POST.get('ip')
            host_name = request.POST.get('host_name')
            project = request.POST.get('project')
            system = request.POST.get('system')
            cpu = request.POST.get('cpu')
            memory = request.POST.get('memory')
            hard = request.POST.get('hard')
            remark = request.POST.get('remark', None)
            logger.info("资产管理,添加数据参数为：{0},{1},{2},{3},{4},{5},{6},{7}".format(
                ip, host_name, project, system, cpu, memory, hard, remark))
            try:
                AssetManagement.objects.create(ip=ip, host_name=host_name, project=project,
                                               system=system, cpu=cpu, memory=memory,
                                               hard=hard, remark=remark)
            except Exception as e:
                logger.error("资产管理添加数据发生异常,异常原因: %s" % e)
                return HttpResponse("添加数据异常")
            logger.info("资产管理添加数据成功,返回添加成功数据")
            # return redirect('/asset/asset/index/0/')
            return HttpResponse("添加成功")
        else:
            logger.info('进入资产 添加 页面')
            return HttpResponse("进入资产添加页面,可以删除了")

    elif option == 'edit_asset':
        logger.info('进入资产管理编辑页面,编辑id为: %s' % id)
        asset_management = AssetManagement.objects.get(id=id)
        if request.method == 'POST':
            asset_management.ip = request.POST.get('ip')
            asset_management.host_name = request.POST.get('host_name')
            asset_management.project = request.POST.get('project')
            asset_management.system = request.POST.get('system')
            asset_management.cpu = request.POST.get('cpu')
            asset_management.memory = request.POST.get('memory')
            asset_management.hard = request.POST.get('hard')
            asset_management.remark = request.POST.get('remark', None)
            asset_management.save()
            logger.info("资产管理更新数据完成,返回成功数据")
            return HttpResponse("更新成功")
        else:
            logger.info("返回资产管理编辑页面")
            return render(request, 'assetApp/asset_manage_edit.html', {'asset': asset_management})

    elif option == 'del_asset':
        logger.info("进入资产管理删除页面,删除id为: %s" % id)
        try:
            AssetManagement.objects.get(id=id).delete()
        except Exception as e:
            logger.info("资产管理删除资产id=[%s]的设备发送异常,异常原因: %s" % (id, e))
        logger.info("资产管理删除资产id=[%s]的设备成功,跳转至首页" % id)
        return redirect('/asset/asset/index/0/')  # 或者 return HttpResponseRedirect('/asset/asset/index/0/')

    elif option == 'index':
        logger.info('进入资产管理展示页面')
        contact_list = AssetManagement.objects.all().order_by('id')     # 获取所有的数据
        logger.info('资产管理对查询结果进行分页')
        contacts = paginatorlist(contact_list, page, pagenumber)
        if pagenumber_switch == 1:
            logger.info('资产管理通过js查询数据，每页显示数量为 %s' % pagenumber)
            contacts = paginatorlist(contact_list, page, pagenumber)
            return render(request, 'assetApp/asset_js_return_page.html', {'asset_management_list': contacts,
                                                                          'page_condition': page_condition})
        logger.info('返回资产管理界面数据到页面')
        return render(request, 'assetApp/asset.html', {'asset_management_list': contacts,
                                                       'page_condition': page_condition})

    elif option == 'search':
        logger.info('资产管理进入查询页面,资产查询内容asset_search=[%s],page=[%s],pagenumber=[%s]' % (asset_search,
                                                                                      page, pagenumber))
        try:
            contact_list = AssetManagement.objects.filter(Q(ip__icontains=asset_search) |
                                                          Q(host_name__icontains=asset_search) |
                                                          Q(project__icontains=asset_search)).order_by('id')
            logger.info("资产管理查询结果进行分页操作")
            contacts = paginatorlist(contact_list, page, pagenumber)
        except Exception as e:
            logger.info("资产管理查询发生异常,异常原因为: %s" % e)
            contacts = ["资产管理查询发生异常,请联系管理员或重新查询"]
        logger.info("资产管理查询结果返回成功")
        return render(request, 'assetApp/asset.html', {'asset_management_list': contacts,
                                                       'page_condition': page_condition})
    else:
        logger.info("资产管理参数错误")
        return HttpResponse('资产管理参数错误')


