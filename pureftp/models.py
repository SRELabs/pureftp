#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models
from server.models import Server
from django.contrib.auth.models import User


class FtpServer(models.Model):
    """
    # ftp server information
    """
    ftp_name = models.CharField(max_length=50)
    server = models.ForeignKey(Server, on_delete='PROTECT')
    ftp_port = models.IntegerField(default=21)
    ftp_description = models.CharField(max_length=255)

    def __str__(self):
        return self.id


class FtpAccount(models.Model):
    """
    # ftp account cluster
    """
    ACCOUNT_STATUS = {
        (0, '活动'),
        (1, '禁用')
    }
    user_id = models.ForeignKey(User, on_delete='PROTECT')
    ftp_server = models.ManyToManyField(FtpServer)
    User = models.CharField(max_length=16, default='')
    status = models.IntegerField(choices=ACCOUNT_STATUS, default=0)
    Password = models.CharField(max_length=64, default='')
    Uid = models.CharField(max_length=16, default='-1')
    Gid = models.CharField(max_length=16, default='-1')
    Dir = models.CharField(max_length=128, default='')
    ULBandwidth = models.SmallIntegerField(default=0)
    DLBandwidth = models.SmallIntegerField(default=0)
    comment = models.CharField(max_length=255)
    ipaccess = models.CharField(default='*', max_length=15)
    QuotaSize = models.SmallIntegerField(default=0)
    QuotaFiles = models.IntegerField(default=0)

    def __str__(self):
        return self.id
