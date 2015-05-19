#!/usr/bin/python
# encoding:utf-8

import sys
import time
import json
import traceback
import collections
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import Task
from util.log.log import log_handler
from util.log.debug import dodebug
from model.user_model import UserModel
from model.log_model import LogModel
from model.log_info_compare import history_info, info_compare, info_create
import ERROR
import URLS


reload(sys)
sys.setdefaultencoding('utf-8')


class BaseHandler(RequestHandler):

    error_code = ERROR
    log = log_handler()
    datatype = 'json'
    filename = ''
    no_valid_token_path = URLS.valid_url_list
    require_log_url = URLS.require_log_url_list

    @coroutine
    def get(self):
        yield Task(self.run)
        self.do_response()

    @coroutine
    def post(self):
        yield Task(self.run)
        self.do_response()

    def do_response(self):
        if self.datatype == 'json':
            data = {'status': '%s' % self.status, 'errstr': self.errstr,
                    'result': self.result}
            jdata = json.dumps(data)
            self.add_header("Content-Type", "application/json;charset=utf-8")
            self.write(jdata)
        else:
            self.write(self.result)

    @coroutine
    def run(self, *args, **kwargs):
        '''返回response'''
        try:
            if self.validate():
                self.do_action()
        except Exception, e:
            self.set_error(self.error_code.API_INTERNAL_ERROR, "服务器内部错误")
            sys.stderr.write(repr(traceback.print_exc()))
            sys.stderr.flush()

    def prepare(self):
        self.request_start_time = time.time()

        self.user_id = self.get_argument("user_id", "")

        if "enterprise_id" in self.request.arguments.keys() and self.get_argument("enterprise_id"):
            self.old_info = history_info(self.get_argument("enterprise_id"))

        self.datatype = 'json'
        self.status = 0
        self.errstr = ''
        self.result = ''
        self.ext_log_data = []

    def set_error(self, err_code, err_str, result=''):
        self.status = '%s' % err_code
        self.errstr = err_str
        self.result = result

    def do_action(self):
        '''handler 重写'''
        return True

    def on_finish(self):
        request_end_time = time.time()
        self.cost_time = int((request_end_time - self.request_start_time)*1000)

        # 设置log的参数
        if self.status == 0:
            self.log.info(self.get_log_info())
            if "/api/record/modify" == self.request.path:
                self.user_modify_log()
            elif "/api/record/create" == self.request.path:
                self.user_create_log()
            elif "/api/user/create" == self.request.path:
                self.user_create_log()
        else:
            self.log.error(self.get_log_info())

    def get_log_info(self):
        try:
            real_ip = self.request.headers.get('X-Real-Ip') or self.request.remote_ip
            cost_time = int((time.time() - self.request_start_time) * 1000)
            log = '\t'.join(["[%s]"] * 9) % (
                real_ip,
                self.request.method,
                self.request.path,
                '&'.join(["%s=%s" % (i, self.get_argument(i)[0:1000]) for i in self.request.arguments.keys()]),
                self.request.headers['User-Agent'],
                self.status,
                self.errstr,
                cost_time,
                '|'.join(self.ext_log_data)
            )
            return log
        except Exception, e:
            return "error when logging: %s" % repr(e)

    def get_status(self):
        return self.status



    #以下函数均为最近添加
    def validate(self):
        #验证用户是否允许请求api
        path = self.request.path
        if path in self.no_valid_token_path:
            return True
        else:
            res = self.verify_user(self.user_id)
            return res

    def verify_user(self, user_id):
        res = UserModel().get({"is_del": 0}, ("user_id",))
        user_id_list = []
        for user in res:
            user_id_list.append(user["user_id"])

        if (self.user_id) and (user_id in user_id_list):
            return True
        else:
            return False



    #用户修改记录
    def user_modify_log(self):
        if self.request.path in self.require_log_url:
            op_object = self.log_argument_deal()
            old_arguments, new_arguments = info_compare(self.old_info, self.modify_info())
            log_bag = dict(
                name=UserModel().get_user_name(self.get_argument('user_id')),
                api=self.request.path,
                ip=self.request.headers.get('X-Real-Ip') or self.request.remote_ip,
                op_object=op_object,
                old_arguments=str(old_arguments),
                arguments=str(new_arguments)
            )
            LogModel().create_log(log_bag)

    #用户创建记录
    def user_create_log(self):
        if self.request.path in self.require_log_url:
            op_object = self.log_argument_deal()
            new_arguments = info_create(self.modify_info())
            log_bag = dict(
                name=UserModel().get_user_name(self.get_argument('user_id')),
                api=self.request.path,
                ip=self.request.headers.get('X-Real-Ip') or self.request.remote_ip,
                op_object=op_object,
                old_arguments="",
                arguments=str(new_arguments)
            )
            LogModel().create_log(log_bag)

    def log_argument_deal(self):
        op_object = ""
        for key in self.request.arguments.keys():
            if key =="enterprise_id":
                op_object = self.get_argument(key)
        return op_object

    def modify_info(self):
        new_argument = collections.defaultdict(dict)
        for key in self.request.arguments.keys():
            if key =="user_id":
                pass
            elif key =="enterprise_id":
                pass
            else:
                new_argument[key] = self.get_argument(key)

        return new_argument
















