#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from lib.ftpaccount_lib import *
from lib.ftpserver_lib import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User
from server.models import Server
from random import choice
from django.db.models import Q
import string
from library.apienc.api_enc import ApiEnc
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test


def super_user_required(login_url=None):
    # return user_passes_test(lambda u: u.is_staff, login_url='/error_403')
    return user_passes_test(lambda u: u.is_superuser, login_url='/error_403')


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_list(request):
    """
    服务器列表
    :param request:
    :return:
    """
    page = int(request.REQUEST.get('page', 1))
    ovs = OpsFtpServer(request.user)
    data = ovs.server_list(page, 40)
    # messages.add_message(request, messages.SUCCESS, 'FTP服务器列表获取成功，如有任何问题，请联系凉白开！')
    return render_to_response('pureftp/s_list.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_add(request):
    """
    添加服务器
    :param request:
    :return:
    """
    msg = ''
    if request.method == 'POST':
        ftp_name = request.REQUEST.get('ftp_name', '')  # 服务器ID
        server_id = request.REQUEST.get('server_id', '')  # Redis端口
        ftp_port = request.REQUEST.get('ftp_port', '')  # Redis端口
        ftp_description = request.REQUEST.get('ftp_description', '')  # redis版本
        ovs = OpsFtpServer(request.user)
        res, msg = ovs.server_add(ftp_name, server_id, ftp_port, ftp_description)
        if res:
            messages.add_message(request, messages.SUCCESS, 'FTP服务器添加成功，如有任何问题，请联系凉白开！')
            return HttpResponseRedirect('/pureftp/s/list/')
    data = Server.objects.all()
    return render_to_response('pureftp/s_add.html',
                              {'data': data, 'msg': msg}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_edit(request):
    msg = ''
    ftp_id = request.REQUEST.get('id', '')
    if request.method == 'POST':
        ftp_name = request.REQUEST.get('ftp_name', '')
        server_id = request.REQUEST.get('server_id', '')
        ftp_port = request.REQUEST.get('ftp_port', '')
        ftp_description = request.REQUEST.get('ftp_description', '')
        ovs = OpsFtpServer(request.user)
        res, msg = ovs.server_edit(ftp_id, ftp_name, server_id, ftp_port, ftp_description)
        if res:
            messages.add_message(request, messages.SUCCESS, 'FTP服务器修改成功，如有任何问题，请联系凉白开！')
            return HttpResponseRedirect('/pureftp/s/list/')
    if ftp_id:
        data = FtpServer.objects.get(pk=ftp_id)
        server_list = Server.objects.all()
        return render_to_response('pureftp/s_edit.html',
                                  {'msg': msg, 'data': data, 'server_list': server_list},
                                  context_instance=RequestContext(request))
    else:
        messages.add_message(request, messages.ERROR, '参数错误，如有任何问题，请联系凉白开！')
        return HttpResponseRedirect('/pureftp/s/list/')


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_del(request):
    """

    :param request:
    :return:
    """
    vpn_id = request.REQUEST.get('id', '')
    if vpn_id:
        ftp_server_info = FtpServer.objects.get(pk=vpn_id)
        account_num = FtpAccount.objects.filter(ftp_server=ftp_server_info).count()
        if account_num < 1:
            msg = 'FTP服务器删除成功！'
            FtpServer.objects.get(pk=vpn_id).delete()
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            msg = '动作：删除FTP服务器，ERROR: 当前SERVER下还有账户，请先删除对应账户或从对应账户中移除当前IP！'
            messages.add_message(request, messages.ERROR, msg)
    else:
        msg = 'ID不存在，删除失败！'
        messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect("/pureftp/s/list/")


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def account_list(request):
    page = int(request.REQUEST.get('page', 1))
    ovs = OpsFtpAccount(request.user)
    data = ovs.account_list(page, 40)
    # messages.add_message(request, messages.INFO, 'FTP所有用户列表获取成功，如有任何问题，请联系凉白开！')
    return render_to_response('pureftp/a_list.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@permission_required('pureftp.pureftp_use', login_url='/error_403')
def account_my_list(request):
    page = int(request.REQUEST.get('page', 1))
    ovs = OpsFtpAccount(request.user)
    data = ovs.account_my_list(page, 40)
    # messages.add_message(request, messages.SUCCESS, 'FTP用户列表获取成功，如有任何问题，请联系凉白开！')
    return render_to_response('pureftp/a_my_list.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def account_add(request):
    msg = ''
    if request.method == 'POST':
        user_id = request.REQUEST.get('user_id', '')
        ftp_id = request.REQUEST.getlist('ftp_id')
        user = request.REQUEST.get('User', '')
        password = request.REQUEST.get('Password', '')
        uid = request.REQUEST.get('Uid', 99)
        gid = request.REQUEST.get('Gid', 99)
        ftp_dir = request.REQUEST.get('Dir', '/tmp/')
        ulbandwidth = request.REQUEST.get('ULBandwidth', 0)
        dlbandwidth = request.REQUEST.get('DLBandwidth', 0)
        comment = request.REQUEST.get('comment', '')
        ipaccess = request.REQUEST.get('ipaccess', '*')
        quotasize = request.REQUEST.get('QuotaSize', 0)
        quotafiles = request.REQUEST.get('QuotaFiles', 0)

        ovs = OpsFtpAccount(request.user)
        res, msg = ovs.account_add(user_id, ftp_id, user, password, uid, gid, ftp_dir, ulbandwidth, dlbandwidth,
                                   comment, ipaccess, quotasize, quotafiles)
        if res:
            messages.add_message(request, messages.SUCCESS, 'FTP用户添加成功，如有任何问题，请联系凉白开！')
            return HttpResponseRedirect('/pureftp/a/list/')
        else:
            messages.add_message(request, messages.ERROR, 'FTP用户添加失败，如有任何问题，请联系凉白开！')
    users = User.objects.all()
    servers = FtpServer.objects.all()
    return render_to_response('pureftp/a_add.html',
                              {'msg': msg, 'password': gen_password(16),
                               'users': users, 'servers': servers}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def account_edit(request):
    account_id = request.REQUEST.get('id', '')
    msg = ''
    if request.method == 'POST':
        user_id = request.REQUEST.get('user_id', '')
        ftp_id = request.REQUEST.getlist('ftp_id')
        user = request.REQUEST.get('User', '')
        password = request.REQUEST.get('Password', '')
        uid = request.REQUEST.get('Uid', 99)
        gid = request.REQUEST.get('Gid', 99)
        ftp_dir = request.REQUEST.get('Dir', '/tmp/')
        ulbandwidth = request.REQUEST.get('ULBandwidth', 0)
        dlbandwidth = request.REQUEST.get('DLBandwidth', 0)
        comment = request.REQUEST.get('comment', '')
        ipaccess = request.REQUEST.get('ipaccess', '*')
        quotasize = request.REQUEST.get('QuotaSize', 0)
        quotafiles = request.REQUEST.get('QuotaFiles', 0)
        ovs = OpsFtpAccount(request.user)
        res, msg = ovs.account_edit(user_id, ftp_id, user, password, uid, gid, ftp_dir, ulbandwidth, dlbandwidth,
                                   comment, ipaccess, quotasize, quotafiles, account_id)
        if res:
            messages.add_message(request, messages.SUCCESS, 'FTP编辑成功，如有任何问题，请联系凉白开！')
            return HttpResponseRedirect('/pureftp/a/list/')
        else:
            messages.add_message(request, messages.ERROR, 'FTP编辑失败，如有任何问题，请联系凉白开！')

    if account_id:
        data = FtpAccount.objects.get(pk=account_id)
        users = User.objects.all()
        servers = FtpServer.objects.all()
        return render_to_response('pureftp/a_edit.html',
                                  {'msg': msg, 'data': data, 'password': gen_password(16),
                                   'users': users, 'servers': servers}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/pureftp/a/list/')


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def account_del(request):
    """
    删除vpn账户
    :param request:
    :return:
    """
    account_id = request.REQUEST.get('id', '')
    if account_id:
        msg = 'FTP用户删除成功，如有任何问题，请联系凉白开！'
        messages.add_message(request, messages.SUCCESS, msg )
        FtpAccount.objects.get(pk=account_id).delete()
    else:
        msg = 'FTP用户删除失败，如有任何问题，请联系凉白开！'
        messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect("/pureftp/a/list/")


def auth(request):
    """
    FTP auth
    :param request:
    :return:
    """
    import json
    user = request.REQUEST.get('user', '')
    password = request.REQUEST.get('password', '')
    ip = request.REQUEST.get('ip', '')
    # 验证sign
    sign = ApiEnc()
    if sign.notify_verify(request.POST):
        response_data = {'code': 0, 'msg': 'fail', 'result': {'auth_ok': 0}}
        data = FtpAccount.objects.get(Q(User=user) & Q(Password=password))
        for d in data.ftp_server.all():
            if d.server.server_ip == ip or d.server.server_internetip == ip:
                response_data['result']['auth_ok'] = 1
                response_data['result']['uid'] = data.Uid
                response_data['result']['gid'] = data.Gid
                response_data['result']['dir'] = data.Dir
                response_data['result']['throttling_bandwidth_ul'] = data.ULBandwidth
                response_data['result']['throttling_bandwidth_dl'] = data.DLBandwidth
                response_data['result']['user_quota_size'] = data.QuotaSize
                response_data['result']['user_quota_files'] = data.QuotaFiles
                # response_data['result']['ratio_upload'] = data
                # response_data['result']['radio_download'] = data.Dir
                # response_data['result']['per_user_max'] = data

                response_data['msg'] = 'success'
                response_data['code'] = 1
                break
    else:
        response_data = {'code': 0, 'msg': 'sign error!', 'result': {'auth_ok': 0}}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def gen_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])
