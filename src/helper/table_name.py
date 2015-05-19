#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    malinger relative const variables
"""


#枚举
def enum(**enums):
    return type('Enum', (), enums)

TableName = enum(
    RECORD="AM_RECORD",
    USER="AM_USER",
    LOG="USER_OP_LOG",
)