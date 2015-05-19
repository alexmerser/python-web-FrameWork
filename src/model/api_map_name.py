#!/usr/bin/python
# -*- coding: utf-8 -*-


import collections
"""
    主要是api和具体名称之间的映射关系
"""

api_to_name = collections.defaultdict(dict)
api_to_name[r"/api/record/modify"] = "修改企业信息"
api_to_name[r"/api/record/create"] = "创建企业"
api_to_name[r"/api/user/create"] = "创建用户"
