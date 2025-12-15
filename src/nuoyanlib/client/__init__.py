# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-15
|
|   「nuoyanlib」客户端库。
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
from ..core.client._lib_client import NuoyanLibClientSystem as _NuoyanLibClientSystem
# from ..core._utils import is_client_wrapper as _is_client_wrapper


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


# _is_client_wrapper = _is_client_wrapper(True)
# distance2nearest_entity = _is_client_wrapper(distance2nearest_entity)
# distance2nearest_player = _is_client_wrapper(distance2nearest_player)


if _clock:
    _consume = (_clock() - _t) * 1000
    _logging.info("Loaded in %.3fms", _consume)
    del _consume


del _logging, _sys, _NuoyanLibClientSystem
del _clock, _t
del _is_client_wrapper
