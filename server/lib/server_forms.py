#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms


class ServerEditForm(forms.Form):
    """修改服务器信息"""
    server_id = forms.CharField(required=True)
    server_name = forms.CharField(required=False)
    server_ip = forms.IPAddressField(required=False)
    server_description = forms.CharField(required=False)


class ServerAddForm(forms.Form):
    """添加服务器信息"""
    server_name = forms.CharField(required=False)
    server_ip = forms.IPAddressField(required=False)
    server_description = forms.CharField(required=False)