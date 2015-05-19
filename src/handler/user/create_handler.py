#!/usr/bin/python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.user_model import UserModel
from util.key_gen.md5_helper import Md5Helper
import json

class UserCreate(BaseHandler):
    """
        user create handler

        user create parameter sample
        {
            "username":"username",  (Required)
            "password":"password",  (Required)
            "type":"0/1"            (Required 0为超级管理员，1为普通账号)
        }
    """

    def do_action(self):
        username = self.get_argument("head_username", "")
        name = self.get_argument("head_name", "")
        password = self.get_argument("head_password", "bdp888888")
        type = int(self.get_argument("head_type", "1"))

        if not (username and name):
            self.set_error(self.error_code.PARAMETERS_INVALID, "must specific username")
            return True

        if UserModel().get({"username": username, "is_del": 0}):
            self.set_error(self.error_code.USER_USERNAME_EXISTS, "same username already exists")
            return True

        user_bag = dict(
            user_id=Md5Helper.key_gen(username),
            name=name,
            username=username,
            password=Md5Helper.ori_str_gen(password),
            type=type
        )

        user_id = UserModel().create_user(user_bag)
        if not user_id:
            self.set_error(self.error_code.API_INTERNAL_ERROR, "create %s user failed" % type)
            return True

        self.result = user_id
        return True

