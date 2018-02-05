# -*- coding:utf-8 -*-
import logging
import logging.handlers

import time

from gs.conf import logger as logconf


def init(logname):
    logging.basicConfig(level=logconf.LEVEL, format=logconf.FORMAT, datefmt=logconf.DATE_FMT, filemode='w+')
    logger = logging.getLogger()
    trfh = logging.handlers.TimedRotatingFileHandler(
        'logs/' + logname + '.' + time.strftime('%Y%m%d%H%M%S', time.localtime())
        + '.log', 'D', 1, 10)
    trfh.setFormatter(logging.Formatter(logconf.FORMAT))
    logger.addHandler(trfh)
