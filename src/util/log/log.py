#!/usr/bin/python
#encoding:utf-8

import os
import logging
import logging.config

from util.conf.conf import get_conf

this_path = os.path.dirname(os.path.abspath(__file__))
default_conf_path = "%s/../../../conf" % this_path
default_log_path = "%s/../../../logs" % this_path

conf_path = os.getenv("CONF", default_conf_path)
conf_file = "%s/logging.conf" % conf_path

logging.config.fileConfig(conf_file, defaults={"logpath":get_conf().get('global', 'log_path')})


def log_handler():
    '''获取日志handler'''
    return logging.getLogger("malinger")


def runtime_log():
    return logging.getLogger("malinger")
