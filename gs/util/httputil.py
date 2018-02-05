# -*- coding:utf-8 -*-

import json

import requests
import requests.packages.urllib3.util.ssl_

from gs.common.cresponse import common_json_entity

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


def invoke_get(path, params=None):
    try:
        res = requests.get(path, params=params)
        return json.loads(res.content)
    except Exception, e:
        print e
        return {}


def invoke_post(path, params=None):
    try:
        if params:
            data = common_json_entity(params)
            headers = {"Content-type": "application/json"}
            res = requests.post(path, data=data, headers=headers)
        else:
            res = requests.post(path)
        return res
    except Exception, e:
        print e
        return ''
