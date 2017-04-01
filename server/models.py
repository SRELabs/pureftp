#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models


class Server(models.Model):
    """
    server information
    """
    server_id = models.AutoField(primary_key=True)
    server_name = models.CharField(max_length=50)
    server_ip = models.CharField(max_length=18)
    server_create_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    server_description = models.CharField(max_length=255)

    def __str__(self):
        return self.server_id
