#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.user_model import UserModel
from util.key_gen.md5_helper import Md5Helper

class UserLogin(BaseHandler):
    """
        user login handler

        user login parameter sample
        {
            "username":"username"
            "password":"password"
        }
    """
    def do_action(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        if not (username and password):
            self.set_error(self.error_code.PARAMETERS_INVALID, "must specific usename and password")
            return True

        password = Md5Helper.ori_str_gen(password)
        user_info = UserModel().verify_user(username, password)

        if not user_info:
            self.set_error(self.error_code.USER_DOMAIN_ERROR, "username or passowrd  error")
            return True

        self.result = {"user_id":user_info["user_id"], "username":user_info["username"], "type":user_info["type"]}
        return True
