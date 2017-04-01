#!/usr/bin/python
# -*- coding:utf-8 -*-

import ConfigParser
import archer.settings


def get_conf(key):
    """
    返回配置文件值
    """
    cf = ConfigParser.ConfigParser()
    if key:
        cf.read(archer.settings.BASE_DIR + '/conf/archer.conf')
        return cf.get('archer', key)
    else:
        return ''

