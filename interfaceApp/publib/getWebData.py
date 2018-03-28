#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/08/29
# Email：
import urllib
import urllib2    # python3.3 不再支持


def postdata():
    values = {"username": "1016903103@qq.com", "password": "XXXX"}
    data = urllib.urlencode(values)
    url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    print(response.read())


def getdata():
    values = {}
    values['username'] = "1016903103@qq.com"
    values['password'] = "XXXX"
    data = urllib.urlencode(values)
    url = "http://passport.csdn.net/account/login"
    geturl = url + "?" + data
    request = urllib2.Request(geturl)
    response = urllib2.urlopen(request)
    print(response.read())


