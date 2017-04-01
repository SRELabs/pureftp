#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')  # 用户ID
    otp = models.CharField(max_length=16, blank=True, null=True, default='')  # 用户Google auth key
    avatar = models.CharField(max_length=255, blank=True, null=True, default='')  # 用户头像

    def __str__(self):
        return self.id

