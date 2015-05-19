#!/usr/bin/python
# encoding:utf-8

#record 模块


#user 模块
from handler.user.create_handler import UserCreate
from handler.user.login_handler import UserLogin
from handler.user.list_head_handler import HeadList

#record 模块
from handler.record.create_handler import RecordCreate
from handler.record.count_handler import AccountCount
from handler.record.info_handler import RecordInfo
from handler.record.list_handler import RecordList
from handler.record.modify_hanler import RecordModify
from handler.record.account_info_handler import AccountInfo

#log 模块
from handler.userlog.info_handler import LogInfo
url_map = [
    #user api
    (r"/api/user/create", UserCreate),
    (r"/api/user/login", UserLogin),
    (r"/api/user/list", HeadList),

    #record api
    (r"/api/record/create", RecordCreate),
    (r"/api/record/count", AccountCount),
    (r"/api/record/info", RecordInfo),
    (r"/api/record/list", RecordList),
    (r"/api/record/modify", RecordModify),
    (r"/api/record/accountinfo", AccountInfo),

    #log api
    (r"/api/log/info", LogInfo)
]
