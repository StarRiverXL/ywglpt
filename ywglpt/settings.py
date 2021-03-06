#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ：2017/12/13
# Email：
"""
Django settings for ywglpt project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# 导入日志相关模块
import logging
import django.utils.log
import logging.handlers
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#y=@t*i24lt%n3ag*8-n)(ugah+_%k^#9d&v3x1%j+u))m_l^x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# * 允许所有机器访问
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'publicApp',
    'assetApp',
    'serversApp',
    'ywdocumentApp',
    'interfaceApp',
    'smallfunApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ywglpt.urls'


# 设置消息框架的级别 注意引入模块
MESSAGE_LEVEL = message_constants.INFO

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ywglpt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'  # 数据库保存时间存在异常
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 解决 while time zone support is active 问题

LOGIN_URL = '/public/login/'

# 参考文章:
# https://www.cnblogs.com/wenjiashe521/archive/2012/11/06/2756779.html
# http://blog.csdn.net/junli_chen/article/details/47335919
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
# 设置的static file的起始url，这个只是在template里边引用到，这个参数和MEDIA_URL的含义相同

STATICFILES_DIRS = (
   # '/var/www/static/',   # 第二选project静态文件搜寻路径，还可以有第三选，第四选……
)
# 和TEMPLATE_DIRS的含义差不多，就是除了各个app的static目录以外还需要管理的静态文件设置，比如项目的公共文件

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# 指明了静态文件的收集目录，即项目根目录（BASE_DIR）下的 static 文件夹。
# 运行上边提到的命令：python manage.py collectstatic 之后静态文件将要复制到的目录，这个目录只有在运行collectstatic时候才会用到

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')     # 设置静态文件路径为主目录下的media文件夹
MEDIA_URL = '/media/'                                               # url映射

# 日志记录相关参数配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {     # 配置打印日志格式
       'standard': {
           'format': '[%(asctime)s] [%(levelname)s] [%(pathname)s '
                     '%(funcName)s %(module)s line:%(lineno)s] %(message)s'}
            # 'format': '[%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] '
            #           '[%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}         # 日志格式
    },
    'filters': {
    },
    'handlers': {       # 用来定义具体处理日志的方式，可以定义多种，"default"就是默认方式，"console"就是打印到控制台方式
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 'filename': "logs\\all.log",     # 日志输出文件  [os.path.join(BASE_DIR, 'templates')],
            'filename': os.path.join(BASE_DIR, "logs", "all.log"),     # 日志输出文件
            'maxBytes': 1024*1024*5,                  # 文件大小
            'backupCount': 5,                         # 备份份数
            'formatter': 'standard',                   # 使用哪种formatters日志格式
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {       # 用来配置用那种handlers来处理日志，比如你同时需要输出日志到文件、控制台。
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'sourceDns.webdns.views': {
            'handlers': ['default', 'mail_admins'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
# 使用方法
# logger = logging.getLogger('sourceDns.webdns.views')    # 对应在 setting.py中配置的logger
# logger.debug()    logger.info()   logger.warning()    logger.error()  logger.critical()




