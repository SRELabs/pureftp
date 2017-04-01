#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from server import views

urlpatterns = patterns('',
                       # server
                       url(r'^list/$', views.server_list, name='server_list'),
                       url(r'^add/$', views.server_add, name='server_add'),
                       url(r'^edit/$', views.server_edit, name='server_edit'),
                       url(r'^del/$', views.server_del, name='server_del'),
                       )
