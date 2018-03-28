from django.shortcuts import render, redirect, HttpResponse
import json, simplejson
# Create your views here.
import logging
from .db import contronl
from .data import temp
from .publib import sendMail
logger = logging.getLogger('django')


def wenming(request):
    # req = {"aa": "c"}
    # return HttpResponse(json.dumps(req))
    # req = simplejson.loads(request.body)
    # return HttpResponse(simplejson.dumps(req))
    key = request.GET.get("key")
    logger.info("wenming接口获取数据,输入参数kew值为：%s" % key)
    value = temp.date.get(key)
    logger.info("wenming文明接口获取数据成功")
    return HttpResponse(simplejson.dumps(value))


def pxy(request, table):
    logger.info("pxy接口获取数据,输入表名为：%s " % table)
    if table == "mjGoodsCategory":
        return HttpResponse(simplejson.dumps(temp.mjGoodsCategory))
    elif table == "mjGoods":
        return HttpResponse(simplejson.dumps(temp.mjGoods))
    else:
        date = {
          "error": " table error"
        }
        return HttpResponse(simplejson.dumps(date))


def dbcontrol(request):
    logger.info("调用数据库接口")
    a = contronl.connet()
    return a


def sendmail(request):
    logger.info("调用邮件发送接口")
    user = request.GET.get("user", None)
    passwd = request.GET.get("passwd", None)
    mail_subject = request.GET.get("subject", None)
    mail_to_list = request.GET.get("list", None)
    mail_content = request.GET.get("content", None)
    if user == "user01" and passwd == "1234qwer":
        try:
            result = sendMail.userSendmail(mail_subject, mail_to_list, mail_content)
            logger.info("邮件发送结果为： %s" %result)
            return HttpResponse("邮件发送成功")
        except Exception as e:
            logger.info("邮件发送失败,原因是： %s" %e)
            return HttpResponse("邮件发送失败，参考样例,访问地址：http://IP:8000/interface/mail/?user=user01"
                                "&passwd=1234qwer&subject=test5&content=test_contet&list=123456789@qq.com")
    else:
        return HttpResponse("用户验证失败,用户为：user01 密码为：1234qwer")



