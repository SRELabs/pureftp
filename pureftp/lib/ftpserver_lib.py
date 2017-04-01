#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pureftp.models import FtpServer
from server.models import Server


class OpsFtpServer:
    """

    """
    user, response_data = None, None

    def __init__(self, user):
        self.user = user
        self.response_data = {
            'pureftp_active': 'active open',
            'menu': 'FTP管理',
            'submenu': '服务器',
            'user': user
        }

    def server_list(self, page, size):
        """
        vpn服务器列表
        :param page:
        :param size:
        :return:
        """
        data = FtpServer.objects.all()
        data, page_range = self.paging(page, data, size)
        self.response_data['data'] = data
        self.response_data['page_range'] = page_range
        return self.response_data

    @staticmethod
    def server_add(ftp_name, server_id, ftp_port, ftp_description):
        """
        add
        :param ftp_name:
        :param server_id:
        :param ftp_port:
        :param ftp_description:
        :return:
        """
        if ftp_name and server_id and ftp_port and ftp_description:
            try:
                FtpServer.objects.get(server=Server.objects.get(pk=server_id))
                return False, 'exists'
            except FtpServer.DoesNotExist:
                vs = FtpServer(ftp_name=ftp_name, server=Server.objects.get(pk=server_id), ftp_port=ftp_port,
                               ftp_description=ftp_description)
                vs.save()
                return True, 'success'
        else:
            return False, 'fail'

    @staticmethod
    def server_edit(ftp_id, ftp_name, server_id, ftp_port, ftp_description):

        if ftp_id and ftp_name and server_id and ftp_port and ftp_description:
            try:
                fs = FtpServer.objects.get(pk=ftp_id)
                fs.server = Server.objects.get(pk=server_id)
                fs.ftp_port = ftp_port
                fs.ftp_description = ftp_description
                fs.ftp_name = ftp_name
                fs.save()
                return True, 'success'
            except FtpServer.DoesNotExist:
                return False, 'Not Exists'
        else:
            return False, 'fail'

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

