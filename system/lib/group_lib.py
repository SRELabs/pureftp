#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.contrib.auth.models import User, Group
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class OpsGroup:
    """

    """
    user, response_data = None, None

    def __init__(self, user):
        self.user = user
        self.response_data = {
            'system_active': 'active open',
            'menu': '系统管理',
            'submenu': '组管理',
            'user': user
        }

    def group_list(self, page, size):
        # 获取发布历史记录
        data = Group.objects.all().order_by('id')
        data, page_range = self.paging(page, data, size)
        self.response_data['page_range'] = page_range
        self.response_data['data'] = data
        return self.response_data

    @staticmethod
    def group_info(self, gid):
        try:
            return Group.objects.get(pk=gid)
        except Group.DoesNotExist:
            return {}

    @staticmethod
    def group_create(form_data):
        name = form_data.get('name')
        permission = form_data.getlist('permission')
        try:
            Group.objects.get(name=name)
            return False, 'GroupIsExists!'
        except Group.DoesNotExist:
            g = Group(name=name)
            g.save()
            for p in permission:
                g.permissions.add(p)
            return True, 'CreateSuccess!'

    @staticmethod
    def group_edit(form_data):
        gid = form_data.get('gid')
        name = form_data.get('name')
        permission = form_data.getlist('permission')
        try:
            g = Group.objects.get(pk=gid)
            g.name = name
            g.permissions = ''
            g.save()
            for p in permission:
                g.permissions.add(p)
            return True, '角色：' + name + '修改成功！'
        except User.DoesNotExist:
            return False,  '橘色：' + name + '不存在！'

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
