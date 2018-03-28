#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2018//
# Email：
from django.shortcuts import render, redirect, HttpResponse
import pymysql, logging
logger = logging.getLogger('django')


def connet():
    db = pymysql.connect(host="120.79.33.57", user="ijiaju_dev", passwd="fsd@f67HD97d#")
    cursor = db.cursor()
    cursor.execute("show databases")
    date = cursor.fetchone()
    logger.info('数据库连接返回结果：%s' % date)
    db.close()
    return HttpResponse("数据库连接成功(OK)")

