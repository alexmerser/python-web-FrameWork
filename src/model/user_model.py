#!/usr/bin/python
# encoding:utf-8

from util.db.mysql_db import DBMalinger
from helper.table_name import TableName


class UserModel:
    """
        Model class of malinger user
            user includes following type
            1. malinger root user (type 0)
            2. malinger normal user (type 1)
    """

    _table = TableName.USER

    def __init__(self):
        self.db = DBMalinger()

    def create_user(self, bag):
        res = self.db.insert_dict(self._table, bag)
        return bag['user_id'] if res else None

    def update(self, conds, update_bag):
        return self.db.update_dict(self._table, update_bag, conds)

    def delete(self, conds):
        updata_bag = {"is_del": 1}
        return self.update(conds, updata_bag)

    def get(self, conds={}, cols="", extra_conds={}):
        return self.db.get(self._table, conds, cols, extra_conds)

    def verify_user(self, username, password):
        sql = """
        select * from %s
        where username = '%s' and password = '%s' and is_del = 0
        """ % (self._table, username, password)
        res = self.db.query(sql)

        if res:
            return res[0]
        else:
            return None

    #根据用户user_id取得用户名
    def get_user_name(self, user_id):
        name = self.get({"user_id":user_id})[0]["name"]
        return name