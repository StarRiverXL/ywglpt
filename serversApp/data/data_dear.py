#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2018/1/4
# Email： 
import logging
import os

# os.path.exists
logger = logging.getLogger('django')


def file_iterator(file, chunk_size=512):
    """
        文件下载读取数据
    : param file: 需要读取的文件名
    : param chunk_size: 文件一次性读取的大小
    : return: 迭代返回读取数据
    """
    logger.info("进入文件读取函数")
    data = {}
    data["safe"] = False
    if not os.path.exists(file):
        logger.info("需要读取的文件：%s 不存在。" % file)
        data["result"] = ["需要读取的文件：%s 不存在。" % file]
        yield data["result"]
    else:
        with open(file, 'rb') as f:
            while True:
                data["result"] = f.read(chunk_size)
                if data["result"]:
                    yield data["result"]
                else:
                    break








