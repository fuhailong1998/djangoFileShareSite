# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@file        : url.py
@author      : Leon(fxkxb.com)
@date        : 2021/7/20 13:12
@description : 
"""
from django.contrib import admin
from django.urls import path, include

from leonsite import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('filelist', views.FileListView.as_view()),
    path('exit', views.ExitView.as_view()),
    path('usercenter', views.UserCenterView.as_view()),
]

