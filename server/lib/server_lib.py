#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from server.models import Server


class OpsServer:
    """
    服务器管理
    """
    user, response_data = None, None

    def __init__(self):
        self.response_data = {}
        self.user = {}

    def list_server(self, page, size):
        """
        服务器列表
        :param size:
        :param page:
        :return:
        """
        data = Server.objects.all()
        data, page_range = self.paging(page, data, size)
        self.response_data['data'] = data
        self.response_data['page_range'] = page_range
        return self.response_data


    @staticmethod
    def add_server(form_data):
        """
        添加服务器
        :param form_data:
        :return:
        """
        server_name = form_data['server_name']
        server_ip = form_data['server_ip']
        server_description = form_data['server_description'] if form_data['server_description'] else ''  # 描述
        try:
            s = Server.objects.get(server_ip=server_ip)
            return False, '机器已经存在，请核实！'
        except Server.DoesNotExist:
            s = Server(server_name=server_name, server_ip=server_ip,
                       server_description=server_description)

            s.save()
            return True, '机器添加成功！'

    @staticmethod
    def set_server_info(form_data):
        """
        添加服务器
        :param form_data:
        :return:
        """
        server_name = form_data['server_name']
        server_ip = form_data['server_ip']
        server_description = '自动'  # 描述
        try:
            s = Server.objects.get(server_ip=server_ip)
            s.server_name = server_name
            s.server_ip = server_ip
            s.save()
            msg = 'server information update success!'
        except Server.DoesNotExist:
            s = Server(server_name=server_name, server_ip=server_ip,
                       server_description=server_description)

            s.save()
            msg = 'server auto reg success!！'
        return True, msg

    @staticmethod
    def add_server_fast(form_data, user_id):
        """
        批量增加主机
        :param form_data:
        :param user_id:
        :return:
        """
        server_list = form_data['server_list']
        msg = '新增结果：'
        flag = True
        for s in server_list.split('\n'):
            server_name = s.split(',')[0].strip()  # 主机名
            server_ip = s.split(',')[1].strip()  # 主机名
            try:
                s = Server.objects.get(server_ip=server_ip)
                flag = False
                msg = msg + '失败：' + server_name.strip() + '|' + server_ip.strip() + ''
            except Server.DoesNotExist:
                s = Server(server_name=server_name, server_ip=server_ip)
            s.save()
        if flag:
            return True, '机器添加成功！'
        else:
            return False, msg

    @staticmethod
    def edit_server(form_data):
        """
        修改服务器
        :param form_data:
        :return:
        """
        s = Server.objects.get(pk=form_data['server_id'])
        s.server_name = form_data['server_name']
        s.server_ip = form_data['server_ip']
        s.server_description = form_data['server_description']
        s.save()
        msg = '服务器资料修改成功，IP：' + s.server_ip
        return True, msg

    def get_server_info(self, server_id):
        data = Server.objects.get(pk=server_id)
        self.response_data['data'] = data
        return self.response_data

    @staticmethod
    def delete(server_id):
        """
        删除服务器
        :param request:
        :return:
        """
        server_info = Server.objects.get(pk=server_id)
        server_ip = server_info.server_ip
        res = server_info.delete()
        code = 0
        return code, '删除成功, IP: ' + server_ip

    @staticmethod
    def paging(page, data, size):
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
