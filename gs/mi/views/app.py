# -*- coding:utf-8 -*-
from flask import request

from gs.common.cresponse import common_json_response
from gs.mi import mi as r_mi
from gs.util import myreq


@r_mi.route('/', methods=['POST'])
def index():
    try:
        signature = myreq.getvalue_from_request('signature')
        data = request.data
        return signature
    except Exception as e:
        print e
