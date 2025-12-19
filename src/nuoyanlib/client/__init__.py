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


from ..core.client.comp import *
from ..core.listener import *
from ..core import error


from .effect import *
from .player import *
from .setting import *
from .sound import *
from .render import *
from .camera import *
from .ui import *


from ..utils import *
from .. import config


for k, v in globals().items():
    if hasattr(v, '_inject_is_client'):
        globals()[k] = v._inject_is_client[0]


if _clock:
    _consume = (_clock() - _t) * 1000
    _logging.info("Loaded in %.3fms", _consume)
    del _consume


del _logging, _sys, _NuoyanLibClientSystem
del _clock, _t
