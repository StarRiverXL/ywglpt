#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time ： 2017/12/06
# Email：
from django import template
from ..models import Navigation

register = template.Library()


@register.simple_tag
def get_navigation():
    return Navigation.objects.all()



