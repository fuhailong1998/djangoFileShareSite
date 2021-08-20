# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@file        : middlewares.py
@author      : Leon(fxkxb.com)
@date        : 2021/8/3 03:21
@description : 
"""
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class IpMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        EXCLUDE_IPS = ['192.168.107.7',
                       '192.168.107.40',
                       '192.168.107.41',
                       '192.168.107.43',
                       '192.168.107.45',
                       '192.168.107.46',
                       '192.168.107.49',
                       '192.168.107.50',
                       '192.168.107.51',
                       '192.168.107.52',
                       '192.168.107.55',
                       '192.168.107.53']
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if ip not in EXCLUDE_IPS:
            return render(request, 'sorry.html')
