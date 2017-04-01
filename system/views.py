#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from library.log_entry import process_logs
from library.config_lib import *
from library.common import paging
from system.models import UserProfile
from system.forms import *
from DjangoCaptcha import Captcha
import pyotp

content_type_id = 5
object_id = 1


def super_user_required(login_url='/error_403'):
    """
    check permission
    :param login_url:
    :return:
    """
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


def user_code(request):
    """
    验证码
    :param request:
    :return:
    """
    ca = Captcha(request)
    ca.type = 'number'
    ca.img_height = 50
    ca.img_width = 300
    return ca.display()


def user_login(request):
    """
    用户登录视图
    :param request:
    :return:
    """
    callback = request.REQUEST.get('next', '')
    response = HttpResponseRedirect(callback) if callback != '' else HttpResponseRedirect('/')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            rs, msg = False, '用户不存在/密码错误！'
            cd = form.cleaned_data
            # check code
            if get_conf('archer_enable_code') == '1' and cd['code']:
                ca = Captcha(request)
                if not ca.check(code=cd['code']):
                    msg = '错误：验证码验证失败！'
            else:
                # 验证账号密码
                user = authenticate(username=cd['username'], password=cd['password'])
                if user:
                    # 验证OTP
                    try:
                        key = user.profile.otp
                        if get_conf('archer_enable_otp') == '1' and cd['otp'] and len(cd['otp']) == 6:
                            if not pyotp.TOTP(key).verify(cd['code']):
                                msg = '错误：动态口令验证失败！'
                        else:
                            login(request, user)
                            rs = True, '登录成功！'
                    except:
                        UserProfile(user=user, otp=pyotp.random_base32(), avatar='').save()  # 追加otp
                        msg = '错误：可能未配置动态口令！'
            if rs:
                process_logs(request.user.id, content_type_id, object_id, request.user.username, ADDITION, msg)
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                messages.add_message(request, messages.ERROR, msg)
                response = HttpResponseRedirect(reverse('system:system_user_login'))
            return response
    else:
        return response if request.user.is_authenticated() else render_to_response('system/login.html', {
            'enable_otp': get_conf('archer_enable_otp'),
            'enable_code': get_conf('archer_enable_code')}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    process_logs(request.user.id, content_type_id, object_id, request.user.username, ADDITION, '用户注销成功')
    logout(request)
    return HttpResponseRedirect(reverse('system:system_user_login'))


@login_required(login_url='/system/u/login/')
def user_change_password(request):
    """
    修改用户密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        rs, msg = False, '密码修改失败'
        if form.is_valid():
            form_data = form.cleaned_data
            new_password1 = form_data['new_password1']
            new_password2 = form_data['new_password2']
            if new_password1 == '' or new_password2 == '':
                msg = "密码/otp_code不允许为空"
            elif new_password1 != new_password2:
                msg = "两次密码不一致"
            elif len(new_password1) < 6:
                msg = "密码必须大于六位"
            elif new_password1 == new_password2:
                request.user.set_password(new_password1)
                request.user.save()
                rs, msg = True, "修改成功"
            else:
                msg = "未知错误"
            process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
            if rs:
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                messages.add_message(request, messages.ERROR, msg)
        else:
            messages.add_message(request, messages.ERROR, '密码不为空！')
        return HttpResponseRedirect(reverse('system:system_user_change_password'))
    else:
        return render_to_response('system/change_password.html', {'userinfo': User.objects.get(pk=request.user.id)},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_list(request):
    """
    User list
    :param request:
    :return:
    """
    page = int(request.REQUEST.get('page', 1))
    data = User.objects.all().order_by('id')
    data, page_range = paging(page, data, 40)
    return render_to_response('system/user_list.html', {'data': data, 'page_range': page_range},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def user_profile(request):
    """
    User Profile
    :param request:
    :return:
    """
    return render_to_response('system/profile.html', {}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_add(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        group = request.POST.get('group', '')
        permission = request.POST.getlist('permission')
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
            res = True
        else:
            msg = '用户已经存在'
            res = False
        process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse('system:system_user_list'))
        else:
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse('system:system_user_add'))
    else:
        groups = Group.objects.all()
        perms = Permission.objects.all()
        return render_to_response('system/create.html',
                                  {'groups': groups, 'perms': perms},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_edit(request, uid):
    if request.method == 'POST':
        uid = request.POST.get('uid', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        group = request.POST.get('group', '')
        permission = request.POST.getlist('permission')
        try:
            u = User.objects.get(pk=uid)
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.groups = group
            u.user_permissions = permission
            u.save()
            res, msg = True, '用户：' + str(uid) + '修改成功！'
        except User.DoesNotExist:
            res, msg = False, '用户：' + str(uid) + '不存在！'
        process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse('system:system_user_list'))
    else:
        data = User.objects.get(pk=uid)
        # group
        groups = Group.objects.all()
        group = data.groups.all()
        # permission
        permissions = Permission.objects.all()
        permission = data.user_permissions.all()
        return render_to_response('system/edit.html',
                                  {'data': data, 'permission': permission,
                                   'permissions': permissions,
                                   'groups': groups, 'group': group}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_otp(request, uid):
    msg = 'OTP修改成功！'
    try:
        data = User.objects.get(pk=uid)
        profile = UserProfile.objects.get(user=data)
        profile.otp = pyotp.random_base32()
        profile.save()
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect(reverse('system:system_user_list'))
    except User.DoesNotExist:
        msg = '用户不存在！'
    except UserProfile.DoesNotExist:
        msg = '用户属性不存在!'
        UserProfile(user=data, otp=pyotp.random_base32(), avatar='').save()
    except Exception, e:
        msg = '未知错误: ' + e.message
    messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect(reverse('system:system_user_list'))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def user_del(request, uid):
    if uid:
        try:
            user = User.objects.get(pk=uid)
            msg = '用户：' + str(user.username) + ', 删除成功！'
            process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
            messages.add_message(request, messages.SUCCESS, msg)
            user.delete()
        except User.DoesNotExist:
            msg = '用户ID: ' + uid + ', 用户不存在！'
            process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
            messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(reverse('system:system_user_list'))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_list(request):
    page = int(request.REQUEST.get('page', 1))
    data = Group.objects.all().order_by('id')
    data, page_range = paging(page, data, 40)
    return render_to_response('system/group_list.html', {'data': data, 'page_range': page_range},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        permission = request.POST.getlist('permission')
        try:
            Group.objects.get(name=name)
            res, msg = False, 'GroupIsExists!'
        except Group.DoesNotExist:
            g = Group(name=name)
            g.permissions = permission
            g.save()
            # for p in permission:
            #     g.permissions.add(p)
            res, msg = True, 'Create Success!'
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)

        return HttpResponseRedirect(reverse('system:system_group_list'))
    else:
        data = Permission.objects.all()
        return render_to_response('system/group_create.html',
                                  {'data': data}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_edit(request, gid):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        name = request.POST.get('name')
        permission = request.POST.getlist('permission')
        try:
            g = Group.objects.get(pk=gid)
            g.name = name
            g.permissions = permission
            g.save()
            res, msg = True, 'role：edit success！'
        except User.DoesNotExist:
            res, msg = False, 'role：not exists！'
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
        return HttpResponseRedirect(reverse('system:system_group_list'))
    else:
        data = Group.objects.get(pk=gid)
        group_perms = data.permissions.all()
        all_perms = Permission.objects.all()
        return render_to_response('system/group_edit.html',
                                  {'data': data, 'group_perms': group_perms,
                                   'all_perms': all_perms}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def group_del(request, gid):
    if gid:
        try:
            group = Group.objects.get(pk=gid)
            msg = '角色：' + str(group.username) + ', 删除成功！'
            process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
            messages.add_message(request, messages.SUCCESS, msg)
            group.delete()
        except Group.DoesNotExist:
            msg = '角色：' + str(gid) + ', 不存在，删除失败！！'
            process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
            messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect(reverse('system:system_group_list'))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_list(request):
    data = Permission.objects.all().order_by('id')
    return render_to_response('system/permit_list.html', {'data': data}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_add(request):
    """
    添加权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        p = Permission()
        p.name = request.POST['name']
        p.codename = request.POST['codename']
        p.content_type_id = request.POST['content_type_id']
        p.save()
        res, msg = True, '权限添加成功，name: ' + request.POST['name'] + ' ,codename' + request.POST['codename']

        page = int(request.REQUEST.get('page', 1))
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        process_logs(request.user.id, content_type_id, object_id, request.user.username, ADDITION, msg)
        return HttpResponseRedirect(reverse('system:system_permit_list') + '?page=' + str(page))
    else:
        content_type_list = ContentType.objects.all()
        return render_to_response('system/permit_add.html', {'content_type_list': content_type_list},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_edit(request, pid):
    if request.method == 'POST':
        pid = request.POST.get('id')
        name = request.POST.get('name')
        try:
            g = Permission.objects.get(pk=pid)
            g.name = name
            g.save()
            res, msg = True, 'Success!'
        except Permission.DoesNotExist:
            res, msg = False, 'PermissionNotExists!'
        if res:
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, msg)
        process_logs(request.user.id, content_type_id, object_id, request.user.username, CHANGE, msg)
        return HttpResponseRedirect(reverse('system:system_permit_list'))
    else:
        data = Permission.objects.get(pk=pid)
        content_type_list = ContentType.objects.all()
        return render_to_response('system/permit_edit.html', {'data': data, 'content_type_list': content_type_list},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def permit_delete(request, pid):
    """
    添加权限
    :param pid:
    :param request:
    :return:
    """
    page = int(request.REQUEST.get('page', 1))
    try:
        Permission.objects.get(pk=pid).delete()
        msg = '删除权限成功，codename：' + p.codename + ', name:' + str(p.name)
        messages.add_message(request, messages.SUCCESS, msg)
    except Permission.DoesNotExist:
        msg = 'PermissionNotExists'
        messages.add_message(request, messages.ERROR, msg)
    process_logs(request.user.id, content_type_id, object_id, request.user.username, DELETION, msg)
    return HttpResponseRedirect(reverse('system:system_permit_list') + '?page=' + str(page))


@login_required(login_url='/system/u/login/')
@super_user_required(login_url="/error_403")
def log_list(request):
    """
    日志审计
    :param request:
    :return:
    """
    page = int(request.REQUEST.get('page', '1'))
    data = LogEntry.objects.all().order_by('-id')
    data, page_range = paging(page, data, 40)
    return render_to_response('system/log_list.html', {'data': data, 'page_range': page_range},
                              context_instance=RequestContext(request))
