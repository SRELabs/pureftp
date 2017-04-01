#!/usr/bin/python
# -*- coding:utf-8 -*-
"""archer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('', url(r'^$', 'archer.views.index', name='home index'),
                       url(r'^home/$', 'archer.views.home', name='home'),
                       url(r'^contact/$', 'archer.views.contact', name='contact'),
                       url(r'^error_403$', 'archer.views.error_403', name='403'),
                       url(r'^error_404$', 'archer.views.error_404', name='404'),
                       url(r'^error_500$', 'archer.views.error_500', name='500'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^server/', include('server.urls')),
                       url(r'^pureftp/', include('pureftp.urls')),
                       url(r'^system/', include('system.urls')),
                       )
