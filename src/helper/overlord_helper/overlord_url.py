#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    overlord manage const variables
"""


#python 枚举实现
def enum(**enums):
    return type('Enum', (), enums)

OverlordUrls = enum(
    account_provision='api/account/provision',
    account_enterprise_list='api/account/enterprise_list',
    enterprise_modify='api/account/enterprise_modify',
    enterprise_info='api/account/enterprise_info',
)


class OverlordClientException(Exception):
    def __init__(self, status, errstr, url=""):
        self.status = status
        self.errstr = errstr
        self.url = url
