# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-20
#  ⠀
# =================================================


from .. import config


try:
    import logging
except ImportError:
    logging = None


if config.ENABLED_LOG and logging:
    class _logger(object):
        def __init__(self, level):
            self.level = level

        def log(self, msg, *args, **kwargs):
            if kwargs.get('show_env', False):
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
        logging.getLogger("Developer").disabled = True
        logging.getLogger("Engine").disabled = True
        logging.getLogger("Part").disabled = True
        # logging.getLogger("mcp").disabled = True




