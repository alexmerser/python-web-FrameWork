#!/usr/bin/env python
# encoding:utf-8

from model.record_model import RecordModel
import collections

#数据库字段对应中文字段值
eng_to_ch = {"contract": "合同金额", "type":"企业类型",
             "head": "商务负责人", "etime": "截止时间",
             "staff_limit": "账号数量", "contact":"企业联系人",
             "domain": "企业域名", "create_user": "创建人",
             "username": "超级管理员", "head_username":"用户名",
             "head_name": "姓名", "head_password": "密码", "head_type": "用户类型",
             "enterprise_name": "企业域名"}


#首先获取历史数据
def history_info(enpterprise_id):
    cols = ("contract", "type", "head", "etime", "staff_limit", "contact", "enterprise_name")
    info = RecordModel().get({"enterprise_id": enpterprise_id}, cols)[0]
    return info


#修改数据和历史数据对比
def info_compare(old_info, new_info):
    old_compared_info = collections.defaultdict(dict)
    new_compared_info = collections.defaultdict(dict)
    for key in new_info.keys():
        if new_info[key] != str(old_info[key]):
            old_compared_info[eng_to_ch[key]] = str(old_info[key])
            new_compared_info[eng_to_ch[key]] = new_info[key]

    old_info_return = '||'.join(["%s=%s" % (i, old_compared_info[i]) for i in old_compared_info.keys()])
    new_info_return = '||'.join(["%s=%s" % (i, new_compared_info[i]) for i in new_compared_info.keys()])
    return old_info_return, new_info_return


def info_create(new_info):
    new_compared_info = collections.defaultdict(dict)
    for key in new_info.keys():
        new_compared_info[eng_to_ch[key]] = new_info[key]

    new_info_return = '||'.join(["%s=%s" % (i, new_compared_info[i]) for i in new_compared_info.keys()])
    return new_info_return