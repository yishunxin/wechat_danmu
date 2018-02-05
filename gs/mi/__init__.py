# -*- coding:utf-8 -*-

from flask import Blueprint

from gs.conf import server

mi = Blueprint('mi', __name__,
               template_folder='templates',
               static_folder='static')

import views
