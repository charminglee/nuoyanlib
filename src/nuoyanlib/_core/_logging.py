# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-05
|
| ==============================================
"""


from time import time, strftime, localtime
from .._core._sys import get_env
from .._core._utils import kwargs_setter
from .._core import _const
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

        @kwargs_setter(show_env=True)
        def log(self, msg, *args, **kwargs):
            ct = time()
            t = strftime("%Y-%m-%d %H:%M:%S", localtime(ct))
            msecs = (ct - int(ct)) * 1000
            s = "%s,%03d" % (t, msecs)
            if kwargs['show_env']:
                print(
                    "[%s] [%s] [nuoyanlib/%s] [%s] %s"
                    % (s, self.level, get_env(), _const.ROOT, msg % args)
                )
            else:
                print(
                    "[%s] [%s] [nuoyanlib] [%s] %s"
                    % (s, self.level, _const.ROOT, msg % args)
                )

    info = _logger("INFO").log
    warning = _logger("WARNING").log
    error = _logger("ERROR").log
    debug = _logger("DEBUG").log

else:
    info = warning = error = debug = lambda *_, **__: None


def disable_modsdk_loggers():
    if logging:
        logging.getLogger("Developer").disabled = 1
        logging.getLogger("Engine").disabled = 1
        logging.getLogger("Part").disabled = 1
        # logging.getLogger("mcp").disabled = 1


if __name__ == "__main__":
    info("test")




