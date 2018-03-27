from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Navigation, SiteNavigation, MonitorPlatform

from django.shortcuts import render, HttpResponse, render_to_response, redirect
from django.conf import settings
from .data.get_auth_code import *
import json, datetime, os, shutil
import logging, platform

logger = logging.getLogger('django')
system_version = platform.system()


def checkuser(request):
    logger.info("进入用户登陆视图")
    # 定义验证码图片保存路径
    today_str = datetime.date.today().strftime("%Y%m%d")  # 20170921
    yesterday_str = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')  # 昨天的时间
    if system_version == "Windows":
        verify_code_img_path = "%s\\media\\public\\authCode\\%s" % (settings.BASE_DIR, today_str)
        yester_code_img_path = "%s\\media\\public\\authCode\\%s" % (settings.BASE_DIR, yesterday_str)
    elif system_version == "Linux":
        verify_code_img_path = "%s/media/public/authCode/%s" % (settings.BASE_DIR, today_str)
        yester_code_img_path = "%s/media/public/authCode/%s" % (settings.BASE_DIR, yesterday_str)
    try:
        if not os.path.isdir(verify_code_img_path):
            os.makedirs(verify_code_img_path)
            shutil.rmtree(yester_code_img_path)  # 删除昨天的验证码图片及文件夹
            logger.info("创建验证码存放路径成功: %s 删除昨天的路径成功: %s" % (verify_code_img_path, yester_code_img_path))
    except Exception as e:
        logger.error("创建保存验证码路径失败，具体原因： %s" % e)
    logger.info("登陆session为: %s" % request.session.session_key)
    # 获取验证码值
    random_filename = gene_text()
    # 生成图片验证码
    random_code = gene_code(verify_code_img_path, random_filename)
    login_info_list = {"code_name": random_filename, "code_img_path": "/media/public/authCode/%s" % today_str}
    # 验证码图片保存结束

    logoutuser = request.GET.get('logoutuser')
    if logoutuser:
        logger.info('退出登陆,用户名:[%s]' % logoutuser)
        logout(request)
        login_info_list['info'] = '退出成功'
    else:
        logger.info('用户未登陆，跳转至登陆界面')
    return render(request, 'publicApp/login.html', {"login_info_list": login_info_list})


def login_ajax(request):
    logger.info("登陆验证,使用ajax方式")
    if request.method == "POST":
        username = request.POST.get('name', None)
        password = request.POST.get('pwd', None)
        _verify_code = request.POST.get("verify_code", None)
        _verify_code_key = request.POST.get("verify_code_key", None)
        logger.info("login_ajax验证 verify_code_key: %s  verify_code: %s" % (_verify_code_key, _verify_code))
        if _verify_code.lower() == _verify_code_key.lower():  # 全部转换为小写字母
            logger.info('登陆验证,使用ajax方式,用户名:[%s] 密码:[%s] ' % (username, password))
            # 验证用户是否存在
            try:
                User.objects.get(username=username).password
            except Exception as e:
                logger.info('登陆验证,使用ajax方式,用户不存在: [%s] 请联系管理员或重新登陆,异常具体原因: %s' % (username, e))
                # messages.add_message(request, messages.INFO, '用户不存在')
                # login_info_list = {'info': '请使用合法用户登陆或联系管理员处理'}
                # return render(request, 'login.html', {'login_info_list': login_info_list})
                data = {"status": False, "failReason": "用户不存在"}
                return HttpResponse(json.dumps(data))
            # 验证用户密码
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info('登陆验证,使用ajax方式,登陆成功,用户名:[%s] 跳转到到系统首页' % username)
                    # 把获取表单的用户名传递给session对象
                    request.session['username'] = username
                    # 设置session过期时间
                    request.session.set_expiry(600)
                    data = {"status": True}
                    return HttpResponse(json.dumps(data))
            else:
                logger.info('登陆验证,使用ajax方式,用户:[%s] 用户名或密码错误' % username)
                messages.add_message(request, messages.WARNING, '密码错误')  # messages 消息框架,使用 ajax 可能无法用到
                data = {"status": False, "failReason": "用户名或密码错误"}
                return HttpResponse(json.dumps(data))
        else:
            logger.info("登陆验证,使用ajax方式,验证码错误")
            data = {"status": False, "failReason": "验证码错误"}
            return HttpResponse(json.dumps(data))


def replase_code(request):
    """
    刷新验证码
    :   param request:
    :   return: 验证码的值
    """
    if request.method == "POST":
        today_str = datetime.date.today().strftime("%Y%m%d")  # 20170921
        if system_version == "Windows":
            verify_code_img_path = "%s\\media\\public\\authCode\\%s" % (settings.BASE_DIR, today_str)
        elif system_version == "Linux":
            verify_code_img_path = "%s/media/public/authCode/%s" % (settings.BASE_DIR, today_str)
        # 获取验证码值
        random_filename = gene_text()
        # 生成图片验证码
        random_code = gene_code(verify_code_img_path, random_filename)
        if random_code:
            logger.info("刷新验证码图片保存成功")
            data = {"code_name": random_filename, "status": True,
                    "code_img_path": "/media/public/authCode/%s/" % today_str}
        else:
            logger.error("刷新验证码图片保存失败")
            data = {"code_name": False, "status": False}
        return HttpResponse(json.dumps(data))


@login_required
def siteindex(request, business):
    logger.info("获取站点导航数据开始")
    # option = request.GET.get('option', None)
    logger.info("站点导航，开始查询[%s]系统导航数据" % business)
    try:
        site_nav = SiteNavigation.objects.filter(business_type=business)
        logger.info("获取 %s 站点导航数据结束" % business)
    except Exception as e:
        logger.error("获取 %s 站点导航数据发生异常,异常原因: %s" % (business, e))
        site_nav = ['获取 %s 站点导航数据发生异常,请联系管理员'% business]
    logger.info("返回 %s 站点导航数据成功" % business)
    return render(request, 'publicApp/site_index.html', {'site_nav_list': site_nav, 'business': business})


@login_required
def indexpage(request):
    logger.info("进入网站首页")
    logger.info("返回首页数据")
    return render(request, 'publicApp/index.html')


def register(request):
    logger.info("进入用户注册页面")
    logger.info("返回用户注册页面数据")
    return render(request, 'publicApp/register.html')


def errorpage(request, number):
    logger.info("返回错误页面,错误码为：%s" % number)
    error_list = {
        "conten2": "Report this?",
        "number": number
    }
    if number == "404":
        error_list["title"] = "Sorry but we couldn't find this page"
        error_list["conten1"] = "This page you are looking for does not exist"
    elif number == "403":
        error_list["title"] = "Access denied"
        error_list["conten1"] = "Full authentication is required to access this resource."
    else:
        error_list["number"] = "500"
        error_list["title"] = "Internal Server Error"
        error_list["conten1"] = "We track these errors automatically, but if the problem persists feel " \
                                "free to contact us. In the meantime, try refreshing.",
    return render(request, 'publicApp/page_error.html', {"error_list": error_list})







