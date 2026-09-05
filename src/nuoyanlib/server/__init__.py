# -*- coding: utf-8 -*-
#  =================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  =================================================


try:
    from time import clock as _clock
    _t = _clock()
except ImportError:
    _clock = None
    _t = 0
from ..core import _logging, _env
from ..core.server._lib_server import NuoyanLibServerSystem as _NuoyanLibServerSystem


_env.check_env("server")
if not _NuoyanLibServerSystem.run():
    _logging.error("NuoyanLibServerSystem run failed!")


from ..core._const import *
from ..core.server.comp import *
from ..core.listener import *
from ..core.error import *


from .entity import *
from .hurt import *
from .inv import *
from .block import *
from .lobby import *


from ..common import *
from .. import config, __version__, __author__, __author_qq__, __author_email__


def __do_inject_is_client(dct):
    for k, v in dct.items():
        if type(v) is type:
            __do_inject_is_client(v.__dict__)
        elif hasattr(v, '_nyl__inject_is_client'):
            dct[k] = v._nyl__inject_is_client[1]


__do_inject_is_client(globals())


if _clock:
    _consume = (_clock() - _t) * 1000 # noqa
    _logging.info("Loaded in %.3fms", _consume)
    del _consume


del (
    _logging,
    _env,
    _NuoyanLibServerSystem,
    _clock,
    _t,
    __do_inject_is_client,
)
