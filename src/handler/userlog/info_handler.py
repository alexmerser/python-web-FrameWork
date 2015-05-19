#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler.base.base_handler import BaseHandler
from model.log_model import LogModel
from model.record_model import RecordModel
from model.api_map_name import api_to_name
import collections
import datetime

class LogInfo(BaseHandler):
    """
        record info handler
        目前是实现是直接返回所有信息
    """

    def do_action(self):
        """
            一些带参数的查询后续做
        """
        log_info = LogModel().get(extra_conds={"order_by": ["time desc"]})
        result = []
        for info in log_info:
            temp = collections.defaultdict(dict)
            info["time"] + datetime.timedelta(hours=8)
            #解决时区问起
            temp["time"] = str(info["time"] + datetime.timedelta(hours=8))
            temp["username"] = info["name"]
            temp["ip"] = info["ip"]
            temp["api"] = api_to_name[info["api"]]
            temp["object"] = RecordModel().get_enterprise_name(info["op_object"]) if info["op_object"] else ""
            temp["arguments"] = info["arguments"]
            temp["old_arguments"] = info["old_arguments"]
            result.append(temp)

        self.result = result
        return True



