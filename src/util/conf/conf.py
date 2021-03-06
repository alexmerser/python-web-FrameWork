#!/usr/bin/python
#encoding:utf-8

import os
import sys
from ConfigParser import RawConfigParser

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Configuration:

    def __init__(self, configfile = None):
        CONF_FILE = "%s/malinger.conf" % os.getenv("CONF")
        self._configFile = CONF_FILE if not configfile else configfile
        self._genConf()

    def _setConfigFile(self, configFile = None):
        '''设置configure文件'''
        self._configFile = configFile
        if not self._configFile:
            raise Exception("配置文件不存在")
        self._genConf()

    def _genConf(self):
        if not self._configFile:
            raise Exception("没有配置文件")
        self._config = RawConfigParser()
        self._config.read(self._configFile)

    def get(self, sect, opt):
        return self._config.get(sect, opt)

def get_conf():
    """创建配置文件"""
    return Configuration()
