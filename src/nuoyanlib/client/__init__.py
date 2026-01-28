# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-19
#  ⠀
# =================================================


try:
    from time import clock as _clock
    _t = _clock()
except ImportError:
    _clock = None
    _t = 0
from ..core import _logging, _sys
from ..core.client._lib_client import NuoyanLibClientSystem as _NuoyanLibClientSystem


_sys.check_env("client")
if not _NuoyanLibClientSystem.register():
    _logging.error("NuoyanLibClientSystem register failed!")


from ..core._const import *
from ..core.client.comp import *
from ..core.listener import *
from ..core.error import *


from .effect import *
from .setting import *
from .render import *
from .camera import *
from .ui import *


from ..utils import *
from .. import config, __version__, __author__, __author_qq__, __author_email__


def __do_inject_is_client(dct):
    for k, v in dct.items():
        if type(v) is type:
            __do_inject_is_client(v.__dict__)
        elif hasattr(v, '_nyl__inject_is_client'):
            dct[k] = v._nyl__inject_is_client[0]

__do_inject_is_client(globals())


if _clock:
    _consume = (_clock() - _t) * 1000
    _logging.info("Loaded in %.3fms", _consume)
    del _consume


del _logging, _sys, _NuoyanLibClientSystem
del _clock, _t
