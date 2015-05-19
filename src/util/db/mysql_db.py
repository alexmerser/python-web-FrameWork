#!/usr/bin/python
# -*- coding: utf-8 -*-

from torndb import Connection
from util.conf.conf import get_conf
import json

class MySQLHelper:

    def __init__(self, host, user, password, database):
        self._db = Connection(host, database, user=user, password=password, max_idle_time=10)
        if not self._db._db:
            raise Exception('%s' % self._db.error_msg)

    def query(self, sql, *parameters):
        return self._db.query(sql, *parameters)

    def query_one(self, sql, *parameters):
        res = self._db.query(sql, *parameters)
        return res.pop() if res else {}

    def write(self, sql, *parameters):
        return self._db.execute(sql, *parameters)

    def gen_insert(self, tablename, rowdict, replace=False):
        return self._db.gen_insert_sql(tablename, rowdict, replace)

    def insert_dict(self, tablename, rowdict):
        key_strs = ", ".join(["""`%s`""" % key for key in rowdict.keys()])
        value_strs = ", ".join(["""'%s'""" % rowdict.get(key) for key in rowdict.keys()])
        sql = """INSERT INTO %s (%s) VALUES (%s)""" % (tablename, key_strs, value_strs)
        return self._db.execute(sql)

    def insert_batch(self, tablename, batch_params):
        value_batch = []
        for param in batch_params:
            keys = param.keys()
            key_strs = ", ".join(["""`%s`""" % key for key in keys])
            value_strs = "(%s)" % ", ".join(
                ["""'%s'""" % "%s" % param.get(key) for key in keys])
            value_batch.append(value_strs)
        sql = """INSERT INTO %s (%s) VALUES %s""" % (tablename, key_strs, ",".join(value_batch))
        return self._db.execute(sql)

    def update_dict(self, tablename, rowdict, where):
        sql = """UPDATE %s SET %s WHERE %s""" % (
        tablename, self._formatter(rowdict, ', '), self._formatter(where, " AND "))
        return self._db.execute(sql)

    def transaction(self, query, parameters):
        return self._db.transaction(query, parameters)

    def get(self, tablename, conds, cols='', extra_conds={}):
        if not tablename:
            return False
        cols = "%s" % ','.join(cols) if cols else '*'
        wheres = []
        values = []
        if conds and isinstance(conds, dict):
            for key, value in conds.items():
                if isinstance(value, (list, tuple)):
                    wheres.append("`%s` IN (%s)" % (key, "'%s'" % "','".join([str(v) for v in value])))
                else:
                    wheres.append("`%s`=%%s" % key)
                    values.append("%s" % value)
        where_str = ' AND '.join(wheres)
        sql = """ SELECT %s FROM `%s` """ % (cols, tablename)
        if where_str:
            sql += """ WHERE %s """ % (where_str)
        if extra_conds.get('group_by'):
            sql += """ GROUP by %s """ % ','.join(extra_conds['group_by'])
        if extra_conds.get('order_by'):
            sql += """ ORDER by %s """ % ','.join(extra_conds['order_by'])
        if extra_conds.get('limit'):
            sql += """ LIMIT %s """ % ','.join(map(str, extra_conds['limit']))

        return self._db.query(sql, *values)


    def _serialize(self, value):
        if isinstance(value, (dict, list, set)):
            value = json.dumps(value)
        else:
            value = "%s" % value
        return value

    def _formatter(self, pairs, delimiter):
        values = []
        for key, value in pairs.items():
            if not isinstance(value, list):
                value = self._serialize(value)
                values.append("""`%s`='%s'""" % (key, value))
            else:
                values.append("""`%s` in ("%s")""" % (key, '","'.join([self._serialize(val) for val in value])))
        return delimiter.join(values)

    def __del__(self):
        self._db.close()

conf = get_conf()
def DBMalinger():
    key = 'malinger_database'
    try:
        return MySQLHelper("%s:%s" % (conf.get(key,"host"), conf.get(key,"port")), conf.get(key,"user"), conf.get(key,"password"), conf.get(key,"database"))
    except:
        return None
