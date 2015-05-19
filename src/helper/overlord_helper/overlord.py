#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
from helper.overlord_helper.overlord_url import OverlordUrls, OverlordClientException
from util.conf.conf import get_conf

reload(sys)
sys.setdefaultencoding('utf-8')


class OverlordClient:
    """
        overlord client
    """
    def __init__(self):
        self.url_prefix = get_conf().get('overlord', 'url')

    def _request(self, short_url, payload):
        url = os.path.join(self.url_prefix, short_url)
        res = requests.post(url, data=payload)
        result = res.json()

        data_params = "&".join(["%s=%s" % (key, payload[key]) for key in payload.keys() if payload[key] is not None])
        repro_url = "%s?%s" % (url,data_params)

        if not result:
            raise OverlordClientException("500", "no result returned from overlord server", repro_url)

        if result['status'] != '0':
            raise OverlordClientException(result['status'], result['errstr'], repro_url)

        return result['result']

    #创建企业账户
    def account_provision(self, domain, contact, mobile, email, username, password, staff_limit):
        params = dict(
            domain=domain,
            contact=contact,
            username=username,
            password=password,
            mobile=mobile,
            email=email,
            staff_limit=staff_limit
        )

        return self._request(OverlordUrls.account_provision, params)

    #显示账号汇总信息
    def account_enterprise_list(self):
        params = dict()

        return self._request(OverlordUrls.account_enterprise_list, params)

    #修改创建企业的相关信息
    def enterprise_modify(self, enterprise_id, contact, staff_limit, is_del):
        params = dict(
            enterprise_id=enterprise_id,
            contact=contact,
            staff_limit=staff_limit,
            is_del=is_del
        )

        return self._request(OverlordUrls.enterprise_modify, params)

    #获取某个企业的相关信息
    def enterprise_info(self, enterprise_id):
        params = dict(
            enterprise_id=enterprise_id,
        )

        return self._request(OverlordUrls.enterprise_info, params)









