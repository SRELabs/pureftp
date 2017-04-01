#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from system import views

urlpatterns = patterns('',
                       # user
                       url(r'^u/login/$', views.user_login, name='system_user_login'),
                       url(r'^u/logout/$', views.user_logout, name='system_user_logout'),
                       url(r'^u/change_password/$', views.user_change_password, name='system_user_change_password'),
                       url(r'^u/list/$', views.user_list, name='system_user_list'),
                       url(r'^u/profile/$', views.user_profile, name='system_user_profile'),
                       url(r'^u/add/$', views.user_add, name='system_user_add'),
                       url(r'^u/del/(\d+)/$', views.user_del, name='system_user_del'),
                       url(r'^u/edit/(\d+)/$', views.user_edit, name='system_user_edit'),
                       url(r'^u/otp/(\d+)/$', views.user_otp, name='system_user_otp'),
                       url(r'^u/code/$', views.user_code, name='system_user_code'),

                       # group
                       url(r'^g/list/$', views.group_list, name='system_group_list'),
                       url(r'^g/add/$', views.group_add, name='system_group_add'),
                       url(r'^g/edit/(\d+)/$', views.group_edit, name='system_group_edit'),
                       url(r'^g/del/(\d+)/$', views.group_del, name='system_group_del'),

                       # permit
                       url(r'^p/list/$', views.permit_list, name='system_permit_list'),
                       url(r'^p/edit/(\d+)/$', views.permit_edit, name='system_permit_edit'),
                       url(r'^p/add/$', views.permit_add, name='system_permit_add'),
                       url(r'^p/del/(\d+)/$', views.permit_delete, name='system_permit_del'),

                       # log
                       url(r'^l/list/$', views.log_list, name='system_log_list'),


                       )

