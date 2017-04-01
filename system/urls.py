#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from system import views

urlpatterns = patterns('',
                       # user
                       url(r'^u/login/$', views.user_login, name='user_login'),
                       url(r'^u/logout/$', views.user_logout, name='user_logout'),
                       url(r'^u/list/$', views.user_list, name='user_list'),
                       url(r'^u/profile/$', views.user_profile, name='user_profile'),
                       url(r'^g/list/$', views.group_list, name='group_list'),
                       url(r'^u/add/$', views.user_create, name='user_create'),
                       url(r'^u/del/$', views.user_del, name='user_del'),
                       url(r'^u/edit/$', views.user_edit, name='user_edit'),

                       # group
                       url(r'^g/add/$', views.group_create, name='group_create'),
                       url(r'^g/edit/$', views.group_edit, name='group_edit'),
                       url(r'^g/del/$', views.group_del, name='group_del'),

                       # permit
                       url(r'^p/list/$', views.permit_list, name='permit_list'),
                       url(r'^p/edit/$', views.permit_edit, name='permit_edit'),
                       url(r'^p/add/$', views.permit_add, name='permit_add'),
                       url(r'^p/del/$', views.permit_delete, name='permit_del'),

                       # log
                       url(r'^l/list/$', views.log_list, name='log_list'),
                       )

