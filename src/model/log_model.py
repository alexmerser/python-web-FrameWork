#!/usr/bin/python
# encoding: utf-8

from util.db.mysql_db import DBMalinger
from helper.table_name import TableName


class LogModel:
    """
        Model class of malinger log
        只针对增、删、改进行操作
    """

    _table = TableName.LOG

    def __init__(self):
        self.db = DBMalinger()

    def create_log(self, bag):
        res = self.db.insert_dict(self._table, bag)
        return res

    def get(self, conds={}, cols="", extra_conds={}):
        return self.db.get(self._table, conds, cols, extra_conds)