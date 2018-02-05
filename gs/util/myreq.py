# -*- coding:utf-8 -*-
from flask import request


def getvalue_from_request(name, default_value=None):
    val = request.form[name] if hasattr(request, 'form') and name in request.form else None
    if val:
        return val
    return request.args[name] if hasattr(request, 'args') and name in request.args else default_value
