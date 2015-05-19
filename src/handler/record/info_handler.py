#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel


class RecordInfo(BaseHandler):
    """
        record info handler

        record info parameter sample
         {
            "enterprise_id":"enterprise_id"  (Required)
         }
    """

    def do_action(self):
        enterprise_id = self.get_argument("enterprise_id", "")
        if not enterprise_id:
            self.set_error(self.error_code.PARAMETERS_INVALID, "missing argumenr enterprise_id")
            return True

        enterprise_info = RecordModel().get({"enterprise_id":enterprise_id}, ("domain", "type", "staff_limit", "contact", "head", "ctime", "etime", "contract", "enterprise_name"))[0]
        if not enterprise_info:
            self.set_error(self.error_code.NORMAL, "the enterprise is not exists")
            return True

        #时间格式这一块要处理，编写时间处理工具
        contract = ""
        if enterprise_info["contract"] == None:
            contract = ""
        else:
            contract = enterprise_info["contract"]
        result = dict(
            enterprise_id=enterprise_id,
            domain=enterprise_info["domain"],
            type=enterprise_info["type"],
            staff_limit=enterprise_info["staff_limit"],
            contact=enterprise_info["contact"],
            head=enterprise_info["head"],
            ctime=str(enterprise_info["ctime"]).split()[0],
            etime=str(enterprise_info["etime"]),
            contract=contract,
            enterprise_name=enterprise_info["enterprise_name"]
        )

        self.result = result
        return True

