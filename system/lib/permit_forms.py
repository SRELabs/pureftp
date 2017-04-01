#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms


class PermitEditForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(required=True)
    codename = forms.CharField(required=False)
    content_type_id = forms.CharField(required=False)


class PermitAddForm(forms.Form):
    name = forms.CharField(required=True)
    codename = forms.CharField(required=False)
    content_type_id = forms.CharField(required=False)