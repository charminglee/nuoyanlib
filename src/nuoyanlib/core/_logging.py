# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from .. import config


try:
    import logging
except ImportError:
    logging = None


LOG_LEVEL_MAP = {
    'ERROR': 3,
    'WARNING': 2,
    'INFO': 1,
    'DEBUG': 0,
}


info = warning = error = debug = lambda *_, **__: None


if config.ENABLED_LOG and logging:
    class _logger(object):
        def __init__(self, level):
            self.level = level

        def log(self, msg, *args, **kwargs):
            if kwargs.get('show_env', False):
                from ..core._env import get_env
                print("[%s] [nuoyanlib] (%s) %s" % (self.level, get_env(), msg % args))
            else:
                print("[%s] [nuoyanlib] %s" % (self.level, msg % args))

    level = LOG_LEVEL_MAP.get(config.LOG_LEVEL, 1)
    if level <= 3:
        error = _logger("ERROR").log
    if level <= 2:
        warning = _logger("WARNING").log
    if level <= 1:
        info = _logger("INFO").log
    if level <= 0:
        debug = _logger("DEBUG").log


def disable_modsdk_loggers():
    if logging:
        logging.getLogger("Developer").disabled = True
        logging.getLogger("Engine").disabled = True
        logging.getLogger("Part").disabled = True
        # logging.getLogger("mcp").disabled = True




