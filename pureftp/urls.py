#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from pureftp import views

urlpatterns = patterns('',
                       # server
                       url(r'^s/add/$', views.server_add, name='server_add'),
                       url(r'^s/list/$', views.server_list, name='server_list'),
                       url(r'^s/edit/$', views.server_edit, name='server_edit'),
                       url(r'^s/del/$', views.server_del, name='server_del'),

                       # account
                       url(r'^a/list/$', views.account_list, name='account_list'),
                       url(r'^a/my/$', views.account_my_list, name='account_my_list'),
                       url(r'^a/add/$', views.account_add, name='account_add'),
                       url(r'^a/edit/$', views.account_edit, name='account_edit'),
                       url(r'^a/del/$', views.account_del, name='account_del'),

                       # API
                       url(r'^api/auth/$', views.auth, name='auth'),
                       )
