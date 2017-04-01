#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required(login_url='/system/u/login/')
def index(request):
    return render_to_response('home/base.html', {}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def home(request):
    data = dict()
    return render_to_response('home/home.html', {'data': data}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def contact(request):
    return render_to_response('home/contact.html', {}, context_instance=RequestContext(request))


def error_403(request):
    return render_to_response('home/403.html', {}, context_instance=RequestContext(request))


def error_404(request):
    return render_to_response('home/404.html', {}, context_instance=RequestContext(request))


def error_500(request):
    return render_to_response('home/500.html', {}, context_instance=RequestContext(request))