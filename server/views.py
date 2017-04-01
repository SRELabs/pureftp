#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from server.lib.server_forms import *
from server.lib.server_lib import *
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import json


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
    page = request.REQUEST.get('page', 1)
    size = 40  # 取消分页
    ops_server = OpsServer()
    data = ops_server.list_server(page, size)
    # 记录日志
    return render_to_response('server/list.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_add(request):
    """
    批量添加服务器
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ServerAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ops_server = OpsServer()
            res, msg = ops_server.add_server_fast(cd, request.user.id)
            # process_logs
            # 前端提示
            if res:
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                # return HttpResponse(msg)
                messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.ERROR, '数据提交不完整！')
        return HttpResponseRedirect('/server/s/list/')
    else:
        users = User.objects.all()
        return render_to_response('server/add.html',
                                  {'users': users},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_edit(request):
    """
    修改服务器信息
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ServerEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ops_server = OpsServer()
            res, msg = ops_server.edit_server(cd)
            # process_logs
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, '参数不足！')
        return HttpResponseRedirect('/server/s/list/')
    else:
        "编辑页面"
        server_id = request.REQUEST.get('server_id', '')
        if server_id == '':
            messages.add_message(request, messages.ERROR, 'server_id异常！')
            return HttpResponseRedirect('/server/s/list/')
        else:
            ops_server = OpsServer()
            data = ops_server.get_server_info(server_id)
            users = User.objects.all()
            data['users'] = users
            return render_to_response('server/edit.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def server_del(request):
    """
    :param request:
    :return:
    """
    response_data = {}
    code = 1
    server_id = request.GET.get('server_id')
    if server_id != '':
        ops_server = OpsServer()
        code, msg = ops_server.delete(server_id)
    else:
        msg = '删除失败, server_id为空'
    messages.add_message(request, messages.INFO, msg)
    # process_logs
    response_data['code'] = code
    return HttpResponse(json.dumps(response_data), content_type="application/json")
