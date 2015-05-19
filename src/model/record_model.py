#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.db.mysql_db import DBMalinger
from helper.table_name import TableName
from time import *
from datetime import *
import os


class RecordModel:
    """
        Model class of malinger record
    """

    _table = TableName.RECORD

    def __init__(self):
        self.db = DBMalinger()

    def create_record(self, bag):
        res = self.db.insert_dict(self._table, bag)
        return bag if res else None

    def update(self, conds, update_bag):
        return self.db.update_dict(self._table, update_bag, conds)

    def get(self, conds={}, cols="", extra_conds={}):
        return self.db.get(self._table, conds, cols, extra_conds)

    def get_own(self, ctime, etime, head, type, enterprise_id_list):
        sql = "select * from %s where " % self._table

        type_sql, head_sql, enterprise_sql, ctime_sql, etime_sql = "", "", "", "", ""
        sql_list = []
        if type:
            type_sql = " type = %s" % int(type)
            sql_list.append(type_sql)
        if head:
            head_sql = " head = '%s' " % head
            sql_list.append(head_sql)
        if enterprise_id_list:
            enterprise_sql = " enterprise_id in (%s) " % "'%s'" % "','".join([str(v) for v in enterprise_id_list])
            sql_list.append(enterprise_sql)
        if ctime:
            ctime_sql = self.time_sql(ctime, 0)
            sql_list.append(ctime_sql)
        if etime:
            etime_sql = self.time_sql(etime, 1)
            sql_list.append(etime_sql)
        sql = sql + " and ".join(sql_list)
        sql = sql + "order by ctime desc,date(etime) asc"

        res = self.db.query(sql)
        return res

    def time_sql(self, date_str, type ):
        date_now = date.today()
        date_sql = " "
        if type == 0:
            if date_str == "0":
                date_compute = date_now - timedelta(7)
                date_sql = date_sql + " ctime > '%s' " % date_compute
            elif date_str == "1":
                date_compute = date_now - timedelta(30)
                date_sql = date_sql + " ctime > '%s' " % date_compute
            elif date_str =="2":
                date_compute = date_now - timedelta(90)
                date_sql = date_sql + " ctime > '%s' " % date_compute
            else:
                date_sql = date_sql + " date(ctime) > '%s' " % date_str
        elif type == 1:
            if date_str == "0":
                date_compute = date_now + timedelta(7)
                date_sql = date_sql + " ('%s' < etime) and (etime < '%s') " % (date_now,date_compute)
            elif date_str == "1":
                date_compute = date_now + timedelta(30)
                date_sql = date_sql + " ('%s' < etime) and (etime < '%s') " % (date_now,date_compute)
            elif date_str =="2":
                date_compute = date_now + timedelta(90)
                date_sql = date_sql + " ('%s' < etime) and (etime < '%s') " % (date_now,date_compute)
            else:
                date_sql = date_sql + " ('%s' < etime) and (etime < '%s') " % (date_now,date_str)

        return date_sql

    def get_enterprise_name(self, enterprise_id):
        domain = self.get({"enterprise_id": enterprise_id})[0]["domain"]
        return domain


