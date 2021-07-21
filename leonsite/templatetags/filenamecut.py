# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@file        : filenamecut.py
@author      : Leon(fxkxb.com)
@date        : 2021/7/21 15:01
@description : 
"""
from django import template

register = template.Library()


@register.filter
def filenamecut(path):

    return str(path)[6:]