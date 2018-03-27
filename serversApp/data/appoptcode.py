#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/26
# Email：
from ..models import appmanagement
from .dingd_message import dd_send_code
from django.db.models import Q
import datetime
import logging
logger = logging.getLogger('django')


class AppOpt(object):
    def __init__(self, **messages):
        self.ipOut = self.__spacedeal(messages['ipOut'])
        self.ipIn = self.__spacedeal(messages['ipIn'])
        self.path = self.__spacedeal(messages['path'])
        self.person = self.__spacedeal(messages['personnel'])   # 运维人员
        self.opt = self.__spacedeal(messages['opt'])     # 操作动作 start stop restart
        self.code = self.__spacedeal(messages['code'])   # 验证码

    def app_opt_control(self):
        """
        APP 操作主控函数
        : return: json格式的提示
        """
        data = {}
        logger.info("进入APP操作主控函数，验证是否需要发送验证码等操作")

        num = 0
        for i in appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)):
            num += 1
            code_state = i.get_code_state_display()
            code_update_time = i.code_update_time
            code_content = i.code_content
            logger.info("数据库记录,操作状态为：[{0}] 上一次修改时间为：[{1}] 当前系统时间为：[{2}] 数据库记录验证码内容为：[{3}] "
                        "本次操作信息 ipIn：[{4}] path：[{5}]".format(code_state, code_update_time, datetime.datetime.now(),
                                                              code_content, self.ipIn, self.path))
        if num == 1:
            if code_state == "None":
                data["result"] = "验证码已发送，请联系运维：%s 获取,谢谢!!!" % self.person
                data["input"] = True
                # dd_send_code("用户：[xxxx] 需要对应用,内网IP:[{0}] 应用路径:[{1}] 进行 [{2}] 操作，"
                #              "验证码为 [123123],请勿泄露给任何人。".format(self.ipIn, self.path, self.opt))
                appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                    code_state=self.opt)   # 记录要操作的动作
                appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                    code_content="123123")  # 记录发送验证码
                appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                    code_send_content="%s" % data["result"])  # 记录发送内容
                appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                    code_content="123123")   # 记录验证码
                logger.info("ipIn:[{0}] path:[{1}] 本次发送验证码为：123123".format(self.ipIn, self.path))
            else:
                if code_state != self.opt:   # 进行功能验证，不允许同时两个动作
                    errorInfo = "已经获取 [{0}] 状态码，暂时不能进行 [{1}] 动作".format(code_state, self.opt)
                    logger.info("本次操作参数为 path:[{0}] ipIn:[{1}], {2}".format(self.path, self.ipIn, errorInfo))
                    data["result"] = errorInfo
                    data["input"] = True
                    return data
                logger.info("本次操作参数为 path:[{0}] ipIn:[{1}] ，web前端获取的验证码为：[{2}]".format(self.path, self.ipIn, self.code))
                if self.code == code_content:  # 验证码验证
                    logger.info("验证通过,开始操作应用,本次操作参数为 path:[{0}] ipIn:[{1}] 动作：[{2}]".format(self.path, self.ipIn, code_state))
                    if code_state == "start":
                        data["result"] = "IP：[%s] 应用：[%s] 已启动" % (self.ipIn, self.path)
                    elif code_state == "stop":
                        data["result"] = "IP：[%s] 应用：[%s] 已停止" % (self.ipIn, self.path)
                    elif code_state == "restart":
                        data["result"] = "IP：[%s] 应用：[%s] 已重启" % (self.ipIn, self.path)
                    else:
                        logger.error("操作保存状态出现异常，具体值为：%s 即将重置状态为为 None" % code_state)
                        data["result"] = "验证出现异常，请重试，若重试仍异常，请联系管理员处理，谢谢。"
                    logger.info("应用已 [{2}]，本次操作参数为：path:[{0}] ipIn:[{1}]".format(self.path, self.ipIn, code_state))
                    appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                        code_state="None")  # 将状态改回 None
                    appmanagement.objects.filter(Q(ipIn__contains=self.ipIn), Q(path__contains=self.path)).update(
                        code_update_time="%s" % datetime.datetime.now())   # 将操作时间修改为当前时间
                    data["input"] = False
                else:
                    data["result"] = "验证码错误，请重新输入！"
                    data["input"] = True
            return data
        else:
            logger.error("非法的请求参数，无法从数据库中获取结果，本次请求参数为：ipOut:[{0}], ipIn:[{1}], path:[{2}], "
                         "person:[{3}], opt:[{4}], code:[{5}]".format(self.ipOut, self.ipIn, self.path,
                                                                      self.person, self.opt, self.code))
            data["result"] = "非法的请求方式,系统已记录你的请求"
            data["input"] = False
            return data

    def __spacedeal(self, avg):
        """
            对通过web页面传送进来的参数去掉前面的空格
        :   return:  原参数不变
        """
        avg2 = ""
        # logger.info("处理前的参数结果为:[%s]" % avg)
        if avg:
            if avg[0:1] == " ":
                avg2 = avg[1:]
            elif avg[0:2] == "  ":
                avg2 = avg[2:]
            else:
                avg2 = avg
        else:
            avg2 = avg
        # logger.info("处理后的参数结果为:[%s]" % avg2)
        return avg2


