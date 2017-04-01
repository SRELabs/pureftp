#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group, Permission


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    next = forms.EmailField(required=False)
    otp = forms.IntegerField(required=False)
    code = forms.IntegerField(required=False)


class UserChangePasswordForm(forms.Form):
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'True'})
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'True'})
        }


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'True'})
        }