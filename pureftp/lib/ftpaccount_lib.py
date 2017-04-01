#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pureftp.models import FtpServer, FtpAccount
from django.contrib.auth.admin import User


class OpsFtpAccount:
    user, response_data = None, None

    def __init__(self, user):
        self.user = user
        self.response_data = {
            'pureftp_active': 'active open',
            'menu': 'FTP管理',
            'submenu': '账户管理',
            'user': user
        }

    def account_list(self, page, size):
        """
        账号列表
        :param page:
        :param size:
        :return:
        """
        data = FtpAccount.objects.all()
        data, page_range = self.paging(page, data, size)
        self.response_data['data'] = data
        self.response_data['page_range'] = page_range
        return self.response_data

    def account_my_list(self, page, size):
        """
        账号列表
        :param page:
        :param size:
        :return:
        """
        data = FtpAccount.objects.filter(user_id=self.user.id)
        data, page_range = self.paging(page, data, size)
        self.response_data['data'] = data
        self.response_data['page_range'] = page_range
        return self.response_data

    @staticmethod
    def account_add(user_id, ftp_id, user, password, uid, gid, ftp_dir, ulbandwidth, dlbandwidth,
                    comment, ipaccess, quotasize, quotafiles):
        if user_id and ftp_id and user and password and ftp_dir:
            try:
                FtpAccount.objects.get(User=user)
                return False, 'exists'
            except FtpAccount.DoesNotExist:
                fa = FtpAccount(user_id=User.objects.get(pk=user_id), User=user, Password=password, Uid=uid, Gid=gid,
                                Dir=ftp_dir, ULBandwidth=ulbandwidth, DLBandwidth=dlbandwidth, comment=comment,
                                ipaccess=ipaccess, QuotaSize=quotasize, QuotaFiles=quotafiles)
                fa.save()
                for f in ftp_id:
                    fa.ftp_server.add(FtpServer.objects.get(pk=f))
                return True, 'success'
        else:
            return False, 'Data Miss!' + user

    @staticmethod
    def account_edit(user_id, ftp_id, user, password, uid, gid, ftp_dir, ulbandwidth, dlbandwidth,
                     comment, ipaccess, quotasize, quotafiles, account_id):
        if user_id and ftp_id and user and password and ftp_dir and account_id:
            try:
                fa = FtpAccount.objects.get(pk=account_id)
                fa.ftp_server = ''
                fa.user_id = User.objects.get(pk=user_id)
                fa.Password = password
                fa.Uid = uid
                fa.Gid = gid
                fa.Dir = ftp_dir
                fa.ULBandwidth = ulbandwidth
                fa.DLBandwidth = dlbandwidth
                fa.comment = comment
                fa.QuotaSize = quotasize
                fa.QuotaFiles = quotafiles
                fa.ipaccess = ipaccess
                fa.save()
                for f in ftp_id:
                    fa.ftp_server.add(FtpServer.objects.get(pk=f))
                return True, 'success'
            except FtpAccount.DoesNotExist:
                return False, 'Not Exists'
        else:
            return False, 'Data Miss!'

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
