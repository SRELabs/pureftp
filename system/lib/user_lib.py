#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from system.models import UserProfile
from library.config_lib import *
import pyotp


class OpsUser:
    user, response_data = None, None

    def __init__(self, user):
        self.user = user
        self.response_data = {
            'system_active': 'active open',
            'menu': '系统管理',
            'submenu': '用户管理',
            'user': user
        }

    def user_login(self, form_data):
        """
        用户登录视图
        :param request:
        :return:
        """
        username = form_data['username']
        password = form_data['password']

        # 验证OTP
        if get_conf('archer_enable_otp') == '1':
            otp = form_data['otp']
            # 获取OTP KEY
            try:
                user_info = User.objects.get(username=username)
                if user_info:
                    try:
                        key = user_info.profile.otp
                        # 验证OTP
                        if not self.auth_otp(key, otp):
                            return False, '错误：动态口令错误！'
                    except UserProfile.DoesNotExist:
                        return False, '错误：未配置OTP'
            except User.DoesNotExist:
                return False, '错误：当前用户不存在！'

        # 验证账号密码
        user = authenticate(username=username, password=password)
        if user:
            info = '登录成功'
            return user, info
        else:
            info = '登录失败：用户名或密码错误！'
        return False, info

    @staticmethod
    def user_changepassword(form_data, user):
        """
        修改用户密码
        :param request:
        :return:
        """
        new_password1 = form_data['new_password1']
        new_password2 = form_data['new_password2']
        if new_password1 == '' or new_password2 == '':
            msg = "密码/otp_code不允许为空"
        elif new_password1 != new_password2:
            msg = "两次密码不一致"
        elif len(new_password1) < 6:
            msg = "密码必须大于六位"
        elif new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            msg = "修改成功"
            return True, msg
        else:
            msg = "未知错误"
        return False, msg

    @staticmethod
    def auth_otp(key, code):
        """
        验证Google code
        :param key:
        :param code:
        :return:
        """
        totp = pyotp.TOTP(key)
        if totp.verify(code):
            return True
        else:
            return False

    def user_list(self, page, size=40):
        data = User.objects.all().order_by('id')
        data, page_range = self.paging(page, data, size)
        self.response_data['data'] = data
        self.response_data['page_range'] = page_range
        return self.response_data

    @staticmethod
    def user_create(form_data):
        username = form_data.get('username', '')
        first_name = form_data.get('first_name', '')
        last_name = form_data.get('last_name', '')
        email = form_data.get('email', '')
        password = form_data.get('password', '')
        group = form_data.get('group', '')
        permission = form_data.getlist('permission')
        user = User.objects.filter(username=username)
        if not user:
            u = User.objects.create_user(username, email, password)
            u.last_name = last_name
            u.first_name = first_name
            u.groups = group
            u.user_permissions = permission
            u.save()
            p = UserProfile(user=u, otp=pyotp.random_base32(), avatar='')
            p.save()
            msg = '创建成功'
            return True, msg
        else:
            msg = '用户已经存在'
            return False, msg

    @staticmethod
    def user_edit(form_data):
        uid = form_data.get('uid', '')
        first_name = form_data.get('first_name', '')
        last_name = form_data.get('last_name', '')
        email = form_data.get('email', '')
        group = form_data.get('group', '')
        permission = form_data.getlist('permission')
        # uid = form_data['uid']
        # first_name = form_data['first_name']
        # last_name = form_data['last_name']
        # email = form_data['email']
        # group = form_data['group']
        # permission = form_data.getlist['permission']
        try:
            u = User.objects.get(pk=uid)
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.groups = group
            u.user_permissions = permission
            u.save()
            return True, '用户：' + str(uid) + '修改成功！'
        except User.DoesNotExist:
            return False,  '用户：' + str(uid) + '不存在！'

    def paging(self, page, data, size):
        """
        分页
        :param page:
        :param data:
        :param size:
        :return:
        """
        # 分页----开始
        paginator = Paginator(data, size)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            data = paginator.page(1)
            page = 1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            data = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        # 分页范围
        after_range_num = 5  # 当前页前显示5页
        before_range_num = 4  # 当前页后显示4页
        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num:page + before_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + before_range_num]
        # 分页----结束
        return data, page_range
