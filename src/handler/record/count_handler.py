#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel
from helper.overlord_helper.overlord import OverlordClient


class AccountCount(BaseHandler):
    """
        统计BDP目前的开户情况
        统计信息包括：1、正式企业数目 2、试用企业数目 3、总得账户数目
    """

    def do_action(self):
        res = OverlordClient().account_enterprise_list()
        if not res:
            self.result = []
            return True

        staff_count = 0
        trial_number = 0
        formal_number = 0
        enterprise_id_list = []
        for enterprise_account in res:
            staff_count += enterprise_account["staff_count"]
            enterprise_id_list.append(enterprise_account["enterprise_id"])

        conds = {"enterprise_id": tuple(enterprise_id_list)}
        enterprise_list = RecordModel().get(conds, ("type",))

        for enterprise in enterprise_list:
            if enterprise['type'] == 0:
                formal_number += 1
            elif enterprise["type"] == 1:
                trial_number += 1

        result = {"formal_number": formal_number, "trial_number": trial_number, "staff_count": staff_count}
        self.result = result
        return True







