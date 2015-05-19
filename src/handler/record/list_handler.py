#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel
from helper.overlord_helper.overlord import OverlordClient
from util.format.date_format import record_date_type
import collections
import datetime


class RecordList(BaseHandler):
    """
        显示目前BDP服务中得企业信息
        企业信息有四种类型:
        1.正式企业账号
        2.试用企业账号
        3.失效企业账号
        4.停用账号
    """

    def do_action(self):
        type = self.get_argument("type", "")
        ctime = self.get_argument("ctime", "")
        etime = self.get_argument("etime", "")
        head = self.get_argument("head", "")

        #首先要根据时间多特殊处理

        res = OverlordClient().account_enterprise_list()
        if not res:
            self.result = []
            return True

        enterprise_id_list = []
        enterprise_id_staff = collections.defaultdict(dict)
        for enterprise_account in res:
            enterprise_id_list.append(enterprise_account["enterprise_id"])
            enterprise_id_staff[enterprise_account["enterprise_id"]] = enterprise_account["staff_count"]
        #拼接查询条件
        """
        conds = collections.defaultdict(dict)
        conds["enterprise_id"] = tuple(enterprise_id_list)
        if type:
            conds["type"] = type
        if head:
            conds["head"] = head

        #enterprise_list = RecordModel().get(conds)
        """
        enterprise_list = RecordModel().get_own(ctime, etime, head, type, enterprise_id_list)

        enterprise_list_info = []
        account_type = {"0":"正式账户","1":"试用账户","2":"失效账户","3":"停用账户"}
        for enterprise in enterprise_list:
            if enterprise["domain"]:
                print enterprise
                enterprise_info = collections.defaultdict(dict)
                enterprise_info["enterprise_id"] = enterprise["enterprise_id"]
                enterprise_info["activate_url"] = enterprise["activate_url"]
                enterprise_info["domain"] = enterprise["domain"]
                if enterprise["contract"] == None:
                    enterprise_info["contract"] = ""
                else:
                    enterprise_info["contract"] = (enterprise["contract"]/float(10000))
                enterprise_info["type"] = account_type[str(enterprise["type"])]
                enterprise_info["create_user"] = enterprise["create_user"]
                enterprise_info["head"] = enterprise["head"]
                #解决时区问题
                enterprise_info["ctime"] = str(enterprise["ctime"] + datetime.timedelta(hours=8)).split()[0]
                enterprise_info["etime"] = str(enterprise["etime"])
                enterprise_info["staff_limit"] = enterprise["staff_limit"]
                enterprise_info["staff_count"] = enterprise_id_staff[enterprise["enterprise_id"]]
                enterprise_info["enterprise_name"] = enterprise["enterprise_name"]
                enterprise_info["contact"] = enterprise["contact"]
                #color_type 需要根据截止之间来定
                #截止时间在一个月内 color_type:1
                #截止时间在不在一个月之内 color_type:0
                enterprise_info["color_type"] = record_date_type(enterprise_info["etime"])
                enterprise_list_info.append(enterprise_info)

        self.result = enterprise_list_info
        return True




