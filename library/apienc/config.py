#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
发布系统，客户端脚本
"""
from library.config_lib import *


class Settings:
    def __init__(self):
        pass

    # 安全检验码，以数字和字母组成的32位字符
    # CS_KEY = '33ikc1t30y2d212a3tm69ot2jyctfi7h'
    CS_KEY = get_conf('archer_md5_sign')

    CS_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    CS_PARTNER = '8217496383490470'

    # 签约支付宝账号或卖家支付宝帐户
    CS_SELLER_EMAIL = 'testn@cloudsa.org'

    CS_SIGN_TYPE = 'MD5'
