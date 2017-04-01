#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class OpsPermit:
    """

    """
    user, response_data = None, None

    def __init__(self, user):
        self.user = user
        self.response_data = {
            'system_active': 'active open',
            'menu': '系统管理',
            'submenu': '权限管理',
            'user': user
        }

    def permit_list(self, page, size):
        # 获取发布历史记录
        data = Permission.objects.all().order_by('id')
        # data, page_range = self.paging(page, data, size)
        # self.response_data['page_range'] = page_range
        self.response_data['data'] = data
        return self.response_data

    @staticmethod
    def permit_info(self, pid):
        try:
            return Permission.objects.get(pk=pid)
        except Permission.DoesNotExist:
            return {}

    @staticmethod
    def permit_add(form_data):
        # try:
        #     permission = Permission.objects.create(codename=form_data.get('codename'),
        #                                            name=form_data.get('name'),
        #                                            content_type=form_data['content_type'])
        # except:
        #     pass
        p = Permission()
        p.name = form_data['name']
        p.codename = form_data['codename']
        p.content_type_id = form_data['content_type_id']
        p.save()
        return True, '权限添加成功，name: ' + form_data['name'] + ' ,codename' + form_data['codename']

    @staticmethod
    def permit_edit(form_data):
        pid = form_data.get('id')
        name = form_data.get('name')
        try:
            g = Permission.objects.get(pk=pid)
            g.name = name
            g.save()
            return True, 'Success!'
        except Permission.DoesNotExist:
            return False, 'PermissionNotExists!'

    @staticmethod
    def permit_delete(form_data):
        pid = form_data['pid']
        try:
            p = Permission.objects.get(pk=pid)
            msg = '删除权限成功，codename：' + p.codename + ', name:' + str(p.name)
            p.delete()

            return True, msg
        except Permission.DoesNotExist:
            return False, 'PermissionNotExists!'

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
