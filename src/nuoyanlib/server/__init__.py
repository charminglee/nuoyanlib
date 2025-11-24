# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-01
|
|   「nuoyanlib」服务端库。
|
| ====================================================
"""


try:
    from time import clock as _clock
    _t = _clock()
except ImportError:
    _clock = None
    _t = 0
from ..core import _logging, _sys
from ..core.server._lib_server import NuoyanLibServerSystem as _NuoyanLibServerSystem


_sys.check_env("server")
if not _NuoyanLibServerSystem.register():
    _logging.error("NuoyanLibServerSystem register failed!")


from ..core.server.comp import *
from ..core.listener import *
from ..core import error


from .entity import *
from .hurt import *
from .inv import *
from .structure import *
from .block import *
from .lobby import *


from ..utils import *
from .. import config


if _clock:
    _consume = (_clock() - _t) * 1000
    _logging.info("Loaded in %.3fms", _consume)
    del _consume


del _logging, _sys, _NuoyanLibServerSystem
del _clock, _t
