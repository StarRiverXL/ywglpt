#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/19

import logging
logger = logging.getLogger('django')


def get_db_data(tablename, ip):
    """
        根据表名获取对应数据
    : param tablename: 表名
    : return: 表数据结果
    """
    logger.info('数据库查询参数, 表名：%s ,查询IP： %s' % (tablename, ip))
    logqueryinfo = []
    try:
        logqueryinfo = tablename.objects.filter(IP=ip)
        logger.info('数据库查询成功，返回结果 %s' % logqueryinfo)
    except Exception as e:
        logger.info('数据库查询失败，具体原因：%s' % e)
    return logqueryinfo







