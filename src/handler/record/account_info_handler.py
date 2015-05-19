#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel
from helper.overlord_helper.overlord import OverlordClient
from util.format.date_format import record_date_type
import collections
import datetime


class AccountInfo(BaseHandler):
    """
        显示目前BDP服务中得企业信息
        企业信息有四种类型:
        1.正式企业账号
        2.试用企业账号
        3.失效企业账号
        4.停用账号
    """

    def do_action(self):
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

        account_info = collections.defaultdict(dict)
        enterprise_list = RecordModel().get(conds={"enterprise_id": enterprise_id_list})

        enterprise_0, enterprise_0_staff_limit, enterprise_0_staff_count = 0, 0, 0
        enterprise_1, enterprise_1_staff_limit, enterprise_1_staff_count = 0, 0, 0
        enterprise_2, enterprise_2_staff_limit, enterprise_2_staff_count = 0, 0, 0
        enterprise_3, enterprise_3_staff_limit, enterprise_3_staff_count = 0, 0, 0

        for enterprise in enterprise_list:
            if enterprise["domain"]:

                if enterprise["type"] == 0:
                    enterprise_0 += 1
                    enterprise_0_staff_limit += enterprise["staff_limit"]
                    enterprise_0_staff_count += int(enterprise_id_staff[enterprise["enterprise_id"]])
                elif enterprise["type"] == 1:
                    enterprise_1 += 1
                    enterprise_1_staff_limit += enterprise["staff_limit"]
                    enterprise_1_staff_count += int(enterprise_id_staff[enterprise["enterprise_id"]])
                elif enterprise["type"] == 2:
                    enterprise_2 += 1
                    enterprise_2_staff_limit += enterprise["staff_limit"]
                    enterprise_2_staff_count += int(enterprise_id_staff[enterprise["enterprise_id"]])
                elif enterprise["type"] == 3:
                    enterprise_3 += 1
                    enterprise_3_staff_limit += enterprise["staff_limit"]
                    enterprise_3_staff_count += int(enterprise_id_staff[enterprise["enterprise_id"]])

        account_info["account_0"] = str(enterprise_0)
        account_info["account_0_staff"] = str(str(enterprise_0_staff_count)+"/"+str(enterprise_0_staff_limit))
        account_info["account_1"] = str(enterprise_1)
        account_info["account_1_staff"] = str(str(enterprise_1_staff_count)+"/"+str(enterprise_1_staff_limit))
        account_info["account_2"] = str(enterprise_2)
        account_info["account_2_staff"] = str(str(enterprise_2_staff_count)+"/"+str(enterprise_2_staff_limit))
        account_info["account_3"] = str(enterprise_3)
        account_info["account_3_staff"] = str(str(enterprise_3_staff_count)+"/"+str(enterprise_3_staff_limit))

        self.result = account_info
        print account_info
        return True
