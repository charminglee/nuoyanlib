# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-09
|
| ==============================================
"""


from time import time, strftime, localtime
from .. import config


__all__ = []


try:
    import logging
except ImportError:
    logging = None


if config.ENABLED_LOG and logging:
    class _logger(object):
        def __init__(self, level):
            self.level = level

        def log(self, msg):
            ct = time()
            t = strftime("%Y-%m-%d %H:%M:%S", localtime(ct))
            msecs = (ct - long(ct)) * 1000
            s = "%s,%03d" % (t, msecs)
            print("[%s] [%s] [nuoyanlib] %s" % (s, self.level, msg))

    info = _logger("INFO").log
    warning = _logger("WARNING").log
    error = _logger("ERROR").log
    debug = _logger("DEBUG").log
else:
    info = lambda *_: None
    warning = lambda *_: None
    error = lambda *_: None
    debug = lambda *_: None


def disable_modsdk_loggers():
    if logging:
        logging.getLogger("Developer").disabled = 1
        logging.getLogger("Engine").disabled = 1
        logging.getLogger("Part").disabled = 1
        # logging.getLogger("mcp").disabled = 1


if __name__ == "__main__":
    info("test")




