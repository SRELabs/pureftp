#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms


class GroupEditForm(forms.Form):
    gid = forms.IntegerField()
    name = forms.CharField(required=False)
    permission = forms.CharField(required=False)


class GroupAddForm(forms.Form):
    name = forms.CharField()
    permission = forms.MultipleChoiceField(required=False, label='permission')
