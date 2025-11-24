# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


from ..core._utils import kwargs_setter
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
            if kwargs['show_env']:
                from ..core._sys import get_env
                print("[%s] [nuoyanlib] (%s) %s" % (self.level, get_env(), msg % args))
            else:
                print("[%s] [nuoyanlib] %s" % (self.level, msg % args))

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




