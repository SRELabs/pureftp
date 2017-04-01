#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
sign验证
"""
from hashlib import md5
import types
from library.apienc.config import Settings
import time


class ApiEnc:
    """
    运维平台客户端
    """
    # 项目信息
    def __init__(self):
        pass

    # 字符串编解码处理
    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    return ' '.join([self.smart_str(arg, encoding, strings_only, errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s

    # 对数组排序并除去数组中的空值和签名参数
    # 返回数组和链接串
    def params_filter(self, params, is_build=True):
        if is_build:
            params['expires'] = int(str(time.time())[0:-3]) + 120
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = self.smart_str(k, Settings.CS_INPUT_CHARSET)
            if k not in ('sign', 'sign_type') and v != '':
                newparams[k] = self.smart_str(v, Settings.CS_INPUT_CHARSET)
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr

    # 生成签名结果,str
    @staticmethod
    def build_mysign_str(prestr, sign_type='MD5'):
        if sign_type == 'MD5':
            return md5(prestr + Settings.CS_KEY).hexdigest()
        return ''

    # 生成签名结果,dict
    def build_mysign(self, data, sign_type='MD5'):
        _, prestr = self.params_filter(data)
        if sign_type == 'MD5':
            return md5(prestr + Settings.CS_KEY).hexdigest()
        return ''

    # 初级验证--签名
    def notify_verify(self, post):
        _, prestr = self.params_filter(post, False)
        mysign = self.build_mysign_str(prestr, Settings.CS_SIGN_TYPE)
        # mysign = self.build_mysign(post)
        if mysign == post.get('sign') and self.expires_verify(post.get('expires', 0)):
            return True
        else:
            return False

    # 请求是否过期
    @staticmethod
    def expires_verify(expires):
        if expires:
            curr_time = int(str(time.time())[0:-3])
            if int(expires) > curr_time:
                return True
        else:
            return False
