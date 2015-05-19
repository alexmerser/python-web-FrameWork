#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import *
from datetime import *

"""
    主要是根据日需要，对日期格式做一些处理
"""

def str_to_date(datestr):
    time_struct = strptime(datestr, "%Y-%m-%d")
    year, month, day = time_struct[0], time_struct[1], time_struct[2]
    return date(year, month, day)


def record_date_type(datestr):
    """
        返回的类型值主要给前端做颜色区别
        2：账户在未来一个月内到期
        1：账户已经到期
        0：正常
    """
    now_date = date.today()
    compute_date = str_to_date(datestr)
    if ( ((compute_date-now_date).days <= 30) and (0<= (compute_date-now_date).days)):
        return 2
    elif((compute_date-now_date).days <= 0):
        return 1
    else:
        return 0



