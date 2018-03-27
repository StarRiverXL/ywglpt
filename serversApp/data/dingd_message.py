#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/12/17
# Email：

# Create your tests here.
import json
from urllib import request, parse
import logging
logger = logging.getLogger('django')


def dd_send_code(content):
    data = {
            "msgtype": "text",
            'text': {
                "content": content
            },
            "at": {
                "atMobiles": [
                    "151xxxxxxxx"
                ],
                "isAtAll": False
            }
        }

    url = r'https://oapi.dingtalk.com/robot/send?access_token=390076113fa1e9f3712c7f6e4b7988' \
          r'bfdafe72cd5981f2a99ba375383883db22'     # 已做修改
    data = bytes(json.dumps(data), "utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # data = parse.urlencode(data).encode('UTF-8')
    req = request.Request(url, data=data, headers=headers)
    page = request.urlopen(req).read()
    data = page.decode('utf-8')
    logger.info("钉钉发送返回结果: %s" % data)
    result = eval(data)
    # result = json.loads(data)  # 同样的结果
    if result["errmsg"] == "ok" and result["errcode"] == 0:
        logger.info("钉钉发送内容：%s,发送成功。" % content)
    else:
        logger.error("钉钉发送内容：%s,发送失败。" % content)

# {"errcode":0,"errmsg":"ok"}    # 返回结果时 str 类型


