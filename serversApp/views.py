#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import json, time, platform
from .data.getlog import GetServerData, ServerOptControl
from .data.getdbinformation import get_db_data
from .data.appoptcode import AppOpt
from .models import viewlog, appmanagement
from .data.data_dear import file_iterator

import logging
logger = logging.getLogger('django')


def download_file(request):
    download_log_name = request.GET.get('download_log_name', None)
    system_version = platform.system()
    if system_version == "Linux":
        logger.info("进入日志下载视图,判断当前操作系统为 linux,成功设置日志路径")
        file_name = "data/downloadlog/%s.log" % download_log_name
    elif system_version == "Windows":
        logger.info("进入日志下载视图,判断当前操作系统为 Windows,成功设置日志路径")
        file_name = "data\\downloadlog\\%s.log" % download_log_name
    else:
        logger.info("进入日志下载视图,判断当前操作系统失败,默认设置windows日志路径")
        file_name = "data\\downloadlog\\%s.log" % download_log_name
    logger.info("进入日志下载视图，请求参数为：%s" % download_log_name)
    response = FileResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("%s.log" % download_log_name)
    logger.info("返回日志下载数据，请求参数为：%s" % download_log_name)
    return response


def serveropt(request):
    logger.info('进入服务器基础操作视图')
    if request.method == 'POST':
        opt = request.GET.get('opt', None)
        ip = request.POST['IP']
        logger.info("服务器基础操作参数,IP=[%s] 操作类型=[%s]" % (ip, opt))
        ip_db_query = get_db_data(tablename=viewlog, ip=ip)     # 提交IP是否在管理范围查询
        logger.info("-------------开始沉睡5秒")
        time.sleep(2)
        logger.info("-------------结束沉睡5秒")
        if ip_db_query.exists():
            logger.info("通过ip=[%s]获取连接服务器的只读用户、密码、SSH端口" % ip)
            for i in ip_db_query:
                ip_username = i.username
                ip_passwd = i.passwd
                ip_ssh_port = i.SSHport
                # 实例化服务器操作
                server = ServerOptControl(ip=ip, ip_username=ip_username, ip_passwd=ip_passwd, ip_port=ip_ssh_port)
            if opt == "2":
                base_cmd = request.POST['base_cmd']  # 基础命令
                base_cmd_content = request.POST['base_cmd_content']  # 基础命令内容
                logger.info("服务器基础操作,本次操作为：基础命令,操作IP=[{0}],选择的基础命令=[{1}],"
                            "填写的基础命令为=[{2}]".format(ip, base_cmd, base_cmd_content))
                data = server.bash_cmd_control(base_cmd, base_cmd_content)
                if data["safe"]:
                    search_messages = data["result"]
                    # logger.info("----------调试返回数据----------%s" % search_messages)
                else:
                    logger.error("服务器基础操作,基础命令执行失败,基础密码为=[%s]" % base_cmd)
                    search_messages = ["基础命令执行失败，请联系管理员处理。"]
            elif opt == "3":
                log_query_type = request.POST['log_query_type']  # 日志查询方式
                log_query_cmd_content = request.POST['log_query_cmd_content']  # 日志查询命令内容
                logger.info("服务器基础操作,本次操作为：日志查询，操作IP：[{0}],查询方式：[{1}]，查询"
                            "命令内容：[{2}]".format(ip, log_query_type, log_query_cmd_content))
                data = server.log_query_control(log_query_type, log_query_cmd_content)
                if data["safe"]:
                    # logger.info("----------调试返回数据----------%s" % data)
                    search_messages = data["result"]
                else:
                    logger.error("日志查询命令执行失败")
                    search_messages = ["日志查询命令执行失败，请联系管理员处理。"]
            elif opt == "4":
                log_download_path = request.POST['log_download_path']  # 日志下载路径
                log_download_begin_line = request.POST['log_download_begin_line']  # 日志下载路径开始行号
                log_download_end_line = request.POST['log_download_end_line']  # 日志下载路径结束行号
                logger.info("服务器基础操作,本次操作为：日志下载，操作IP：[{0}],日志下载路径：[{1}],日志下载路径开始、"
                            "结束行号：[{2}:{3}]".format(ip, log_download_path, log_download_begin_line,
                                                    log_download_end_line))
                data = server.log_download_control(log_download_path, log_download_begin_line, log_download_end_line)
                if data["safe"]:
                    # logger.info("----------调试返回数据----------%s" % data)
                    if data["safe_number"]:
                        return HttpResponse('<a href="http://127.0.0.1:8000/servers/downloadlog/?download'
                                            '_log_name=%s">点我获取日志</a>' % data["result"])
                    else:
                        search_messages = data["result"]
                else:
                    logger.error("日志下载命令执行失败")
                    search_messages = ["日志下载命令执行失败，请联系管理员处理。"]
            else:
                search_messages = ['不支持的基础操作方式，不支持的请求。']
        else:
            logger.info("服务器基础操作 IP=[%s] 在数据库 viewlog 表中不存在,请联系管理员添加" % ip)
            search_messages = ["IP=[%s] 地址不在管理范围,请联系管理员添加" % ip]
        logger.info('服务器基础操作返回查询结果')
        return render(request, 'serversApp/serveropt_jquery_return.html', {"log": search_messages})
    else:
        logger.info("返回服务器基础操作页面")
        return render(request, 'serversApp/serveropt.html')


def appopt(request, option):
    """
        app详情页面展示及操作相关动作
    : param request:
    : param option: 表示动作
    : return:
    """
    logger.info("进入应用管理视图")
    # 获取需要操作的IP和路径
    ipOut = request.GET.get('ipOut', None)
    ipIn = request.GET.get('ipIn', None)
    path = request.GET.get('path', None)
    personnel = request.GET.get('personnel', None)
    opt = request.GET.get('opt', None)
    code = request.GET.get('code', None)
    if option == "index":
        logger.info("进入应用管理展示界面")
        app_list = appmanagement.objects.all().order_by('id')
        logger.info('应用管理数据库查询,返回数据给页面')
        return render(request, 'serversApp/appmanagement.html', {'app_list': app_list})
    if option == 'action_get' and path:
        logger.info('页面操作传入相关参数,应用外网IP=[{0}] 内网IP=[{1}] 部署路径=[{2}] 对应运维=[{3}] '
                    '执行动作=[{4}]'.format(ipOut, ipIn, path, personnel, opt))
        appopt = AppOpt(ipOut=ipOut, ipIn=ipIn, path=path, personnel=personnel, opt=opt, code=code)
        data = appopt.app_opt_control()
        return HttpResponse(json.dumps(data))
    logger.info("返回应用管理视图页面")
    return render(request, 'serversApp/appmanagement.html')






