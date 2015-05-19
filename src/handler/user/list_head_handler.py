#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.user_model import UserModel

class HeadList(BaseHandler):
    """
        List of Head (获取商务负责人名单)
    """

    def do_action(self):
        res = UserModel().get({"is_del":0, "type":1}, ("name",))

        head_list = []
        if not res:
            self.result = head_list
            return True

        for head in res:
            head_list.append(head["name"])

        self.result = head_list
        return True




