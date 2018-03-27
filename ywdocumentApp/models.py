#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017//
# Email：
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown, math


class Category(models.Model):
    name = models.CharField('分类名', max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', auto_now=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    img = models.ImageField(upload_to='img/ywdocument', blank=True, null=True)     # 上传的图片
    img_name = models.CharField(max_length=20, blank=True, null=True)   # 图片说明
    file = models.FileField(upload_to='file/ywdocument', blank=True, null=True)    # 上传的附件

    def get_absolute_url(self):
        page_num = 2  # 分页时每页的页数 需要根据view中index的类视图函数而设置.
        page = 1  # 设置默认需要请求的页
        if int(self.pk) >= int(page_num):
            page = math.ceil(self.pk / page_num)    # 向上取整
        return reverse('ywdocument:detail', kwargs={'pk': self.pk, 'page': page})

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

