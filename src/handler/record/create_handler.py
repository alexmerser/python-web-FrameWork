#!/user/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.record_model import RecordModel
from util.key_gen.md5_helper import Md5Helper
from helper.overlord_helper.overlord import OverlordClient
import json


class RecordCreate(BaseHandler):
    """
        Record create handler

        record create parameter sample
        {
            "domain":"domain"           (Required)
            "contact":"contact"         (Required)
            "mobile":"mobile"
            "email":"email"
            "username":"username"       (Default "admin")
            "password":"password"       (Default "888888")
            "staff_limit":"staff_limit" (Default 5)
            "type":"type"               (Required 0:正式账号 1：试用账号)
            "head":"head"               (Required )
            "etime":"etime"
            "contract":"contract"       (Default "尚未敲定")
            "create_user":"create_user" (Required)
        }
    """

    def do_action(self):
        domain = self.get_argument("domain", "")
        contact = self.get_argument("contact", "管理员")
        mobile = self.get_argument("mobile", "")
        email = self.get_argument("email", "")
        username = self.get_argument("username", "admin")
        password = self.get_argument("password", "888888")
        staff_limit = self.get_argument("staff_limit", "5")
        type = self.get_argument("type", "")
        head = self.get_argument("head", "")
        etime = self.get_argument("etime", "")
        # contract = self.get_argument("contract", "尚未敲定")
        # create_user = self.get_argument("create_user", "")
        enterprise_name = self.get_argument("enterprise_name", "")

        if not (domain and contact and type and head and etime and username and enterprise_name):
            self.set_error(self.error_code.PARAMETERS_INVALID, "please confirm arguments")
            return True

        #首先在BDP中创建企业账户
        result = OverlordClient().account_provision(domain, contact, mobile, email, username, password, staff_limit)
        enterprise_id = result["enterprise_id"]
        url = result["activate_url"]
        if not enterprise_id:
            self.set_error(self.error_code.NORMAL, "failure of creating enterprise")
            return True
        # if contract == "":
        enterprise_bag = dict(
            enterprise_id=enterprise_id,
            domain=domain,
            contact=contact,
            type=type,
            head=head,
            etime=etime,
            staff_limit=staff_limit,
            enterprise_name=enterprise_name,
            activate_url=url,
        )
        # else:
        #     enterprise_bag = dict(
        #         enterprise_id=enterprise_id,
        #         domain=domain,
        #         contact=contact,
        #         type=type,
        #         head=head,
        #         etime=etime,
        #         staff_limit=staff_limit,
        #         contract=contract,
        #         enterprise_name=enterprise_name,
        #         activate_url=url,
        #     )
        res = RecordModel().create_record(enterprise_bag)
        if not res:
            self.set_error(self.error_code.NORMAL, "failure of creating record")
            self.result = "failed"
            return True

        self.result = "success"
        return True

