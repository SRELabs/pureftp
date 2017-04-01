#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from system.lib.permit_lib import *
from system.lib.group_lib import *
from system.lib.user_lib import *
from system.lib.log_lib import *
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import urllib
import urllib2
import json


def super_user_required(login_url=None):
    # return user_passes_test(lambda u: u.is_staff, login_url='/error_403')
    return user_passes_test(lambda u: u.is_superuser, login_url='/error_403')


def post_data(data, url):
    """
    POST方法
    :param data:
    :param url:
    :return:
    """
    content = ''
    try:
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, {})
        req.add_header('User-Agent', 'archer_ftp V1.0.1')
        response = urllib2.urlopen(req)
        content = json.load(response)
    except:
        print 'Http接口请求异常!'
    return content


def user_login(request):
    """
    用户登录视图
    :param request:
    :return:
    """

    archer_st = request.COOKIES.get('ARCHER_ST', '')
    st = request.REQUEST.get('st', '')
    response = HttpResponseRedirect('/')
    if st:
        # login
        response.set_cookie('ARCHER_ST', value=st, path='/')
        return response
    elif request.user.is_authenticated():
        return response
    elif archer_st:
        data = dict()
        data['st'] = archer_st
        user = post_data(data, get_conf('archer_passport_user'))
        if user:
            try:
                user = User.objects.get(username=user['users_name'])
            except User.DoesNotExist:
                user = User.objects.create_user(user['users_name'], user['users_name']+'@archer.xin', 'aa123456')
                user.is_superuser = True
                user.is_staff = True
                user.save()
            user = authenticate(username=user.username, password='')
            login(request, user)
        else:
            print archer_st
            response.delete_cookie('ARCHER_ST', path='/')
        return response
    else:
        return HttpResponseRedirect(get_conf('archer_passport_login') + '?app_id=' + get_conf('app_id') +
                                    '&next=/system/u/login')


@login_required(login_url='/system/u/login/')
def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    # process_logs
    response = HttpResponseRedirect(get_conf('archer_passport_logout'))
    response.delete_cookie('ARCHER_ST', path='/')
    logout(request)
    return response


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_list(request):
    page = int(request.REQUEST.get('page', 1))
    ops_server = OpsUser(request.user)
    data = ops_server.user_list(page, 40)
    return render_to_response('system/user_list.html', data)


@login_required(login_url='/system/u/login/')
def user_profile(request):
    return render_to_response('system/profile.html', {}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_create(request):
    if request.method == 'POST':
        ops_server = OpsUser(request.user)
        res, msg = ops_server.user_create(request.POST)
        # 前端提示
        messages.add_message(request, messages.SUCCESS, msg)
        if res:
            return HttpResponseRedirect('/system/u/list')
        else:
            return HttpResponseRedirect('/system/u/add')
    else:
        groups = Group.objects.all()
        perms = Permission.objects.all()
        return render_to_response('system/create.html',
                                  { 'groups': groups, 'perms': perms}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_edit(request):
    uid = request.REQUEST.get('uid', '')
    if request.method == 'POST':
        ops_server = OpsUser(request.user)
        res, msg = ops_server.user_edit(request.POST)
        # 前端提示
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect('/system/u/list/')
    else:
        data = User.objects.get(pk=uid)
        # group
        groups = Group.objects.all()
        group = data.groups.all()
        # permission
        permissions = Permission.objects.all()
        permission = data.user_permissions.all()
        return render_to_response('system/edit.html',
                                  {'data': data, 'permission': permission,'permissions': permissions,'groups': groups,
                                   'group': group})


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_del(request):
    uid = request.REQUEST.get('uid', '')
    if uid:
        try:
            user = User.objects.get(pk=uid)
            msg = '用户：' + user.username + ', 删除成功！'
            messages.add_message(request, messages.SUCCESS, msg)
            user.delete()
        except User.DoesNotExist:
            msg = '用户ID: ' + uid + ', 用户不存在！'
            messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect('/system/u/list/')


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_list(request):
    page = int(request.REQUEST.get('page', 1))
    ops_server = OpsGroup(request.user)
    data = ops_server.group_list(page, 40)
    return render_to_response('system/group_list.html', data)


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_create(request):
    if request.method == 'POST':
        ops_server = OpsGroup(request.user)
        res, msg = ops_server.group_create(request.POST)
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)

        return HttpResponseRedirect('/system/g/list/')
    else:
        data = Permission.objects.all()
        return render_to_response('system/group_create.html', {'data': data}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_edit(request):
    if request.method == 'POST':
        # form = GroupEditForm(request.POST)
        # if form.is_valid():
        # cd = form.cleaned_data
        ops_server = OpsGroup(request.user)
        res, msg = ops_server.group_edit(request.POST)
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect('/system/g/list/')
    else:
        gid = request.REQUEST.get('gid', '')
        data = Group.objects.get(pk=gid)
        group_perms = data.permissions.all()
        all_perms = Permission.objects.all()
        return render_to_response('system/group_edit.html',
                                  {'data': data, 'group_perms': group_perms,
                                   'all_perms': all_perms})


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_del(request):
    gid = request.REQUEST.get('gid', '')
    if gid:
        try:
            group = Group.objects.get(pk=gid)
            msg = '角色：' + group.username + ', 删除成功！'
            messages.add_message(request, messages.SUCCESS, msg)
            group.delete()
        except Group.DoesNotExist:
            msg = '角色：' + gid + ', 不存在，删除失败！！'
            messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect('/system/g/list/')


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_list(request):
    page = int(request.REQUEST.get('page', 1))
    ops_permit = OpsPermit(request.user)
    data = ops_permit.permit_list(page, 20)
    return render_to_response('system/permit_list.html', data, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        ops_permit = OpsPermit(request.user)
        res, msg = ops_permit.permit_add(request.POST)
        page = int(request.REQUEST.get('page', 1))
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect('/system/p/list/?page=' + str(page))
    else:
        content_type_list = ContentType.objects.all()
        return render_to_response('system/permit_add.html', {'content_type_list': content_type_list},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_edit(request):
    if request.method == 'POST':
        ops_permit = OpsPermit(request.user)
        res, msg = ops_permit.permit_edit(request.POST)
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect('/system/p/list/')
    else:
        pid = request.REQUEST.get('id', '')
        data = Permission.objects.get(pk=pid)
        content_type_list = ContentType.objects.all()
        return render_to_response('system/permit_edit.html', {'data': data, 'content_type_list': content_type_list})


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_delete(request):
    """
    添加权限
    :param request:
    :return:
    """
    ops_permit = OpsPermit(request.user)
    res, msg = ops_permit.permit_delete(request.GET)
    page = int(request.REQUEST.get('page', 1))
    if res:
        messages.add_message(request, messages.SUCCESS, msg)
    else:
        messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect('/system/p/list/?page=' + str(page))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def log_list(request):
    lid = request.REQUEST.get('id', '')
    page = int(request.REQUEST.get('page', '1'))
    ops_permit = OpsLog(request.user)
    data = ops_permit.log_list(page, 20)
    return render_to_response('system/log_list.html', data, context_instance=RequestContext(request))
