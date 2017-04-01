#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    next = forms.EmailField(required=False)
    otp = forms.IntegerField(required=False)


class UserChangePasswordForm(forms.Form):
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()


class UserAddForm(forms.Form):
    username = forms.CharField()
    password = forms.EmailField()
    first_name = forms.EmailField(required=False)
    email = forms.CharField(required=False)
    group = forms.CharField(required=False)
    permission = forms.CharField(required=False)


class UserEditForm(forms.Form):
    uid = forms.IntegerField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    group = forms.CharField(required=False)
    permission = forms.CharField(required=False)

