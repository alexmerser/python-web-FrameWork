#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel
from helper.overlord_helper.overlord import OverlordClient

class RecordModify(BaseHandler):
    """
        record modify handler

        record modify parameter sample
        {
            "enterprise_id":"enterprise_id"  (Required)
            "type":"type"                    (Required)
            "staff_limit":"staff_limit"      (Required)
            "contact":"contact"              (Required)
            "head":"head"                    (Required)
            "etime":"etime"                  (Required)
            "contract":"contract"            (Required)
        }
    """

    def do_action(self):
        enterprise_id = self.get_argument("enterprise_id", "")
        type = self.get_argument("type", "")
        staff_limit = self.get_argument("staff_limit", "")
        contact = self.get_argument("contact", "管理员")
        head = self.get_argument("head", "")
        etime = self.get_argument("etime", "")
        # contract = self.get_argument("contract", "")
        enterprise_name = self.get_argument("enterprise_name", "")

        bool_args = (enterprise_id and type and staff_limit and enterprise_name and head and etime)
        if not bool_args:
            self.set_error(self.error_code.PARAMETERS_INVALID, "pleas the number and context of arguments right")
            return True

        ol_res = OverlordClient().enterprise_info(enterprise_id)
        if not ol_res:
            self.set_error(self.error_code.NORMAL, "the enterprise information is not exists")
            return True
        # if contract == "":
        update_bag = dict(
            type=type,
            staff_limit=staff_limit,
            head=head,
            etime=etime,
            enterprise_name=enterprise_name
        )
        # else:
        #     update_bag = dict(
        #         type=type,
        #         staff_limit=staff_limit,
        #         head=head,
        #         etime=etime,
        #         contract=contract,
        #         enterprise_name=enterprise_name
        #     )
        res = RecordModel().update({"enterprise_id": enterprise_id}, update_bag)
        if res:
            self.set_error(self.error_code.NORMAL, "modify record failure")
            self.result = "failure"
            return True

        is_del = 0

        if type == "0" or type == "1":
            is_del = 0
        else:
            is_del = 1

        overlord_res = OverlordClient().enterprise_modify(enterprise_id, contact, staff_limit, is_del)
        if not overlord_res:
            self.set_error(self.error_code.NORMAL, "overlord modify record failure")
            self.result = "failure"
            return True

        self.result = "success"
        return True
